import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd
from collaberative_filtering import collaborative_recommendation
from hybrid_recomender import hybrid_rec
from pathlib import Path


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
    
# Simple direct method - avoids multiple download attempts
    try:
        # Use a placeholder to show loading state
        with st.empty():
            st.write("Loading audio...")
            # Direct approach with timeout
            st.audio(url, format="audio/mp3")
    except Exception:
        # Fallback to just providing a link
        st.write("Audio preview couldn't be loaded automatically")
        st.markdown(f"[Open audio in new tab]({url})")

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