# import streamlit as st
# import requests
# import json
# import time
# import os

# st.title("Spotify Audio Diagnostic Tool")

# # Test URL - Use one that you know works locally
# test_url = "https://p.scdn.co/mp3-preview/4d26180e6961fd46866cd9106936ea55dfcbaa75?cid=774b29d4f13844c495f206cafdad9c86"

# st.write("### 1. Testing URL Accessibility")
# st.code(test_url, language="text")

# # Check if we can access the URL
# try:
#     start_time = time.time()
#     response = requests.head(test_url, timeout=10)
#     end_time = time.time()
    
#     st.write(f"URL Response Code: {response.status_code}")
#     st.write(f"Response Time: {end_time - start_time:.2f} seconds")
    
#     if response.status_code == 200:
#         st.success("✅ URL is accessible from the container")
#     else:
#         st.error(f"❌ URL returned status code {response.status_code}")
#         st.write("Response Headers:")
#         st.code(json.dumps(dict(response.headers), indent=2), language="json")
# except Exception as e:
#     st.error(f"❌ Error accessing URL: {str(e)}")

# st.write("### 2. Testing Environment")
# st.write(f"Python version: {os.popen('python --version').read().strip()}")
# st.write(f"Container hostname: {os.popen('hostname').read().strip()}")
# st.write(f"Network connectivity: {os.popen('ping -c 1 8.8.8.8 || echo \"Ping failed\"').read().strip()}")
# st.write(f"DNS resolution: {os.popen('nslookup p.scdn.co || echo \"DNS lookup failed\"').read().strip()}")

# st.write("### 3. Testing Audio Playback Methods")

# st.write("#### Method 1: Native Streamlit Audio")
# try:
#     st.audio(test_url, format="audio/mp3")
#     st.write("Did you hear any audio? If not, this method failed.")
# except Exception as e:
#     st.error(f"Error: {str(e)}")

# st.write("#### Method 2: HTML5 Audio Player")
# try:
#     html = f"""
#     <audio controls style="width: 100%;">
#         <source src="{test_url}" type="audio/mpeg">
#         Your browser does not support the audio element.
#     </audio>
#     """
#     st.markdown(html, unsafe_allow_html=True)
#     st.write("Did you hear any audio? If not, this method failed.")
# except Exception as e:
#     st.error(f"Error: {str(e)}")

# st.write("#### Method 3: Direct Download and Play")
# try:
#     response = requests.get(test_url, timeout=10)
#     if response.status_code == 200:
#         audio_bytes = response.content
#         st.write(f"Downloaded {len(audio_bytes)} bytes of audio data")
#         st.audio(audio_bytes, format="audio/mp3")
#         st.write("Did you hear any audio? If not, this method failed.")
#     else:
#         st.error(f"Failed to download audio: Status code {response.status_code}")
# except Exception as e:
#     st.error(f"Error: {str(e)}")

# st.write("### 4. Browser Console Information")
# st.write("""
# Please open your browser's developer tools (F12 or right-click -> Inspect) and check the Console tab for any errors related to audio playback. 
# Common errors include:
# - CORS policy violations
# - Mixed content warnings
# - Network failures
# """)

# st.write("### 5. Workaround Solution")
# st.write("""
# If none of the above methods work, try this workaround:
# 1. Add a proxy server to your app that fetches the audio and serves it locally
# 2. Use HTTPS for your Streamlit app
# 3. Use a different audio player library
# """)

# proxy_code = """
# # Example proxy endpoint in Flask
# from flask import Flask, request, Response
# import requests

# app = Flask(__name__)

# @app.route('/proxy-audio')
# def proxy_audio():
#     url = request.args.get('url')
#     if not url:
#         return "Missing URL parameter", 400
    
#     try:
#         response = requests.get(url, stream=True)
#         return Response(
#             response.iter_content(chunk_size=1024),
#             content_type=response.headers['Content-Type']
#         )
#     except Exception as e:
#         return str(e), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
# """

# st.code(proxy_code, language="python")





import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd
from collaberative_filtering import collaborative_recommendation
from hybrid_recomender import hybrid_rec
from pathlib import Path
import requests
from io import BytesIO

# Enhanced audio player function with multiple fallback methods
def display_audio_player(url):
    """
    Enhanced audio player function for Spotify preview URLs with multiple fallback methods
    
    Parameters:
    - url: Spotify preview URL string
    """
    if not url:
        st.write("No preview available for this song")
        return
    
    # First attempt: Direct download and play from memory
    try:
        with st.spinner("Loading audio..."):
            response = requests.get(url, timeout=10)
            
        if response.status_code == 200:
            audio_bytes = response.content
            st.audio(audio_bytes, format="audio/mp3")
            return  # Exit if successful
        else:
            st.warning(f"Could not download audio (Status: {response.status_code}). Trying alternative methods...")
    except Exception as e:
        st.warning(f"Download failed: {str(e)}. Trying alternative methods...")
    
    # Second attempt: Direct streaming via Streamlit's audio component
    try:
        st.audio(url, format="audio/mp3")
    except Exception as e:
        st.warning(f"Streamlit audio player failed. Trying HTML5 player...")
    
    # Third attempt: HTML5 audio player
    try:
        html = f"""
        <audio controls style="width: 100%;">
            <source src="{url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"All playback methods failed")
    
    # Always provide a direct link as final fallback
    st.markdown(f"[Open audio in new tab]({url})", unsafe_allow_html=True)
    
    # Add troubleshooting expander
    with st.expander("Audio not playing? Troubleshooting tips"):
        st.write("1. Check your browser's console for CORS errors (Press F12 > Console tab)")
        st.write("2. Try opening the link in a new tab to test direct access")
        st.write("3. Ensure your browser allows audio playback")
        st.write("4. If using a VPN or proxy, try disabling it")
        
        if st.button("Test URL Accessibility"):
            try:
                import time
                start_time = time.time()
                test_response = requests.head(url, timeout=5)
                end_time = time.time()
                
                st.write(f"URL Response: {test_response.status_code}")
                st.write(f"Response Time: {(end_time - start_time):.2f} seconds")
                
                if test_response.status_code == 200:
                    st.success("✅ URL is accessible")
                else:
                    st.error(f"❌ URL returned status code {test_response.status_code}")
            except Exception as e:
                st.error(f"❌ Error testing URL: {str(e)}")

# path
transformed_data_path = "data/transformed_data.npz"
cleaned_data_path = "data/cleaned_data.csv"
path_item_user_mat_collab = Path.cwd() / "data" / "item_user_matrix.npz"
path_filtered_songs = Path.cwd() / "data" / "filtered_songs.csv"
path_mat_content = Path.cwd() / "data" / "content_based.npz"

# load the data
if 'songs_data' not in st.session_state:
    st.session_state.songs_data = pd.read_csv(cleaned_data_path)
    
if 'filtered_songs_df' not in st.session_state:
    st.session_state.filtered_songs_df = pd.read_csv(path_filtered_songs)

# load the transformed data for only content based and collaborative filtering- interaction matrix
if 'transformed_data' not in st.session_state:
    st.session_state.transformed_data = load_npz(transformed_data_path)
    
if 'collab_interaction_matrix' not in st.session_state:
    st.session_state.collab_interaction_matrix = load_npz(path_item_user_mat_collab)
    
if 'content_interaction_matrix' not in st.session_state:
    st.session_state.content_interaction_matrix = load_npz(path_mat_content)

# Title
st.title('Welcome to the Spotify Song Recommender!')

# Subheader
st.write('### Enter the name of a song and the recommender will suggest similar songs 🎵🎧')

# Text Input
song_name = st.text_input('Enter a song name:')
st.write('You entered:', song_name)
# artist name
artist_name = st.text_input('Enter the artist name:')
st.write('You entered:', artist_name)

# Check if inputs are not empty
if song_name and artist_name:
    # lower case 
    song_name = song_name.strip().lower()
    artist_name = artist_name.strip().lower()
    
    # k recommndations
    k = st.selectbox('How many recommendations do you want?', [5,10,15,20], index=1)
    
    if ((st.session_state.filtered_songs_df["name"] == song_name) & (st.session_state.filtered_songs_df["artist"] == artist_name)).any():
        # type of filtering
        filtering_type = st.selectbox('Select the type of filtering', ['Collaborative Filtering','Hybrid Filtering'],index=0)
    
        # diversity slider
        diversity = st.slider('Diversity of Recommendations', min_value=1, max_value=10, value=5, step=1)
    
        content_based_weight = 1 - diversity/10
        collaborative_weight = diversity/10
    else:
        # type of filtering
        filtering_type = st.selectbox('Select the type of filtering', ['Content Based Filtering'])
    
    # Button
    if filtering_type == 'Content Based Filtering':
        if st.button('Get Recommendations'):
            if ((st.session_state.songs_data['name'] == song_name) & (st.session_state.songs_data['artist'] == artist_name)).any():
                st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
                recommendations = recommend(song_name, artist_name, st.session_state.songs_data, st.session_state.transformed_data, k)
            
                # Display Recommendations
                for ind, recommendation in recommendations.iterrows():
                    song_name_display = recommendation['name'].title()
                    artist_name_display = recommendation['artist'].title()
                    
                    if ind == 0:
                        st.markdown("## Currently Playing")
                        st.markdown(f"#### **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
                    elif ind == 1:   
                        st.markdown("### Next Up 🎵")
                        st.markdown(f"#### {ind}. **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
                    else:
                        st.markdown(f"#### {ind}. **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
            else:
                st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")
    
    elif filtering_type == 'Collaborative Filtering':
        if st.button('Get Recommendations'):
            if ((st.session_state.filtered_songs_df["name"] == song_name) & (st.session_state.filtered_songs_df["artist"] == artist_name)).any():
                st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
                recommendations = collaborative_recommendation(song_name,
                                            artist_name,
                                          st.session_state.filtered_songs_df,
                                          st.session_state.collab_interaction_matrix,
                                          k=k)
                
                # Display Recommendations
                for ind, recommendation in recommendations.iterrows():
                    song_name_display = recommendation['name'].title()
                    artist_name_display = recommendation['artist'].title()
                    
                    if ind == 0:
                        st.markdown("## Currently Playing")
                        st.markdown(f"#### **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
                    elif ind == 1:   
                        st.markdown("### Next Up 🎵")
                        st.markdown(f"#### {ind}. **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
                    else:
                        st.markdown(f"#### {ind}. **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
            else:
                st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")
    
    elif filtering_type == 'Hybrid Filtering':
        if st.button('Get Recommendations'):
            if ((st.session_state.filtered_songs_df["name"] == song_name) & (st.session_state.filtered_songs_df["artist"] == artist_name)).any():
                st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
                recommendations = hybrid_rec(song_name, artist_name, st.session_state.filtered_songs_df, 
                                             st.session_state.collab_interaction_matrix, 
                                             st.session_state.content_interaction_matrix,
                                             k, content_based_weight, collaborative_weight)
                
                # Display Recommendations
                for ind, recommendation in recommendations.iterrows():
                    song_name_display = recommendation['name'].title()
                    artist_name_display = recommendation['artist'].title()
                    
                    if ind == 0:
                        st.markdown("## Currently Playing")
                        st.markdown(f"#### **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
                    elif ind == 1:   
                        st.markdown("### Next Up 🎵")
                        st.markdown(f"#### {ind}. **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
                    else:
                        st.markdown(f"#### {ind}. **{song_name_display}** by **{artist_name_display}**")
                        display_audio_player(recommendation['spotify_preview_url'])
                        st.write('---')
            else:
                st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")
else:
    st.info("Please enter both a song name and artist name to get recommendations.")