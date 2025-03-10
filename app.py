import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd
from collaberative_filtering import collaborative_recommendation
from pathlib import Path


# Content based filtering

# transformed data path
transformed_data_path = "data/transformed_data.npz"

# cleaned data path
cleaned_data_path = "data/cleaned_data.csv"

# load the data
songs_data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data = load_npz(transformed_data_path)


# collaberative filtering
path_item_user_mat = Path.cwd() / "data" / "item_user_matrix.npz"
path_filtered_songs = Path.cwd() / "data" / "filtered_songs.csv"
path_utliity_df = Path.cwd() / "data" / "utility_df.csv"

#Load the sparse matrix
interaction_matrix = load_npz(path_item_user_mat)
filtered_songs_df = pd.read_csv(path_filtered_songs)
utility_df = pd.read_csv(path_utliity_df)

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

# lower case 
song_name = song_name.strip().lower()
artist_name = artist_name.strip().lower()

# k recommndations
k = st.selectbox('How many recommendations do you want?', [5,10,15,20], index=1)

# type of filtering
filtering_type = st.selectbox('Select the type of filtering', ['Content Based Filtering','Collaborative Filtering'])

# # Button
if filtering_type == 'Content Based Filtering':
    if st.button('Get Recommendations'):
        if ((songs_data['name'] == song_name) & (songs_data['artist'] == artist_name)).any():
            st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
            recommendations = recommend(song_name,artist_name,songs_data,transformed_data,k)
        
            # Display Recommendations
            for ind , recommendation in recommendations.iterrows():
                song_name = recommendation['name'].title()
                artist_name = recommendation['artist'].title()
                
                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{song_name}** by **{artist_name}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                elif ind == 1:   
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                else:
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
        else:
            st.write(f"Sorry ,we couldn't find {song_name} in our db . Please try another song")

elif filtering_type == 'Collaborative Filtering':
    if st.button('Get Recommendations'):
        if ((filtered_songs_df["name"] == song_name) & (filtered_songs_df["artist"] == artist_name)).any():
            st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
            recommendations = collaborative_recommendation(song_name,
                                        artist_name,
                                        utility_df,
                                      filtered_songs_df,
                                      interaction_matrix,
                                      k=k)
            
            
            
            # Display Recommendations
            for ind , recommendation in recommendations.iterrows():
                song_name = recommendation['name'].title()
                artist_name = recommendation['artist'].title()
                
                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{song_name}** by **{artist_name}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                elif ind == 1:   
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                else:
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
        else:
            st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")