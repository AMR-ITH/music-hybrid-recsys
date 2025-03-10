import numpy as np
import pandas as pd
import joblib
import logging
import sys
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from category_encoders.count import CountEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz, csr_matrix
from pathlib import Path

# Configure logging to console and file
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("content_filtering.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def train_transformer(data, frequency_encode_cols, ohe_cols, tfidf_col, standard_scale_cols, min_max_scale_cols):
    """
    Trains and saves a ColumnTransformer for data preprocessing.
    """
    try:
        transformer = ColumnTransformer(
            transformers=[
                ("frequency_encode", CountEncoder(normalize=True, return_df=True), frequency_encode_cols),
                ("ohe", OneHotEncoder(handle_unknown="ignore"), ohe_cols),
                ("tfidf", TfidfVectorizer(max_features=85), tfidf_col),
                ("standard_scale", StandardScaler(), standard_scale_cols),
                ("min_max_scale", MinMaxScaler(), min_max_scale_cols)
            ],
            remainder='passthrough',
            n_jobs=-1
        )

        logging.info("Fitting the transformer...")
        transformer.fit(data)
        joblib.dump(transformer, "transformer.joblib")
        logging.info("Transformer saved successfully.")
    except Exception as e:
        logging.error(f"Error in train_transformer: {e}", exc_info=True)




def data_for_content_filtering(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the input DataFrame by dropping specific columns.
    This function removes the columns "track_id", "name", and "spotify_preview_url"
    from the provided DataFrame.

    Parameters:
    data (pd.DataFrame): The input DataFrame containing music track information.

    Returns:
    pd.DataFrame: A DataFrame with the specified columns removed.
    """
    logging.debug("Applying content-based filtering...")

    filtered_data = data.drop(columns=["track_id", "name", "spotify_preview_url"], errors="ignore")

    logging.info("Content-based filtering applied successfully.")
    return filtered_data


def transform_data(data):
    """
    Loads the trained transformer and applies transformations to new data.
    """
    try:
        logging.info("Loading transformer...")
        transformer = joblib.load("transformer.joblib")
        logging.info("Transforming data...")
        transformed_data = transformer.transform(data)

        if not isinstance(transformed_data, csr_matrix):
            transformed_data = csr_matrix(transformed_data)
        
        logging.info("Data transformation completed.")
        return transformed_data
    except Exception as e:
        logging.error(f"Error in transform_data: {e}", exc_info=True)
        return None

def save_transformed_data(transformed_data, save_path):
    """
    Saves transformed data as a sparse matrix.
    """
    try:
        logging.info(f"Saving transformed data to {save_path}...")
        save_npz(save_path, transformed_data)
        logging.info("Transformed data saved successfully.")
    except Exception as e:
        logging.error(f"Error in save_transformed_data: {e}", exc_info=True)

def recommend(song_name,artist_name, songs_data, transformed_data, k=10):
    """
    Recommends top k songs similar to the given song.
    """
    try:
        song_name = song_name.strip().lower()
        song_row = songs_data[(songs_data["name"].str.lower() == song_name) & (songs_data["artist"].str.lower() == artist_name)]

        if song_row.empty:
            logging.warning(f"Song '{song_name}' not found.")
            return None

        song_index = song_row.index[0]
        input_vector = transformed_data[song_index].reshape(1, -1)
        similarity_scores = cosine_similarity(input_vector, transformed_data)
        top_k_songs_indexes = np.argsort(similarity_scores.ravel())[-k:][::-1]
        top_k_songs = songs_data.iloc[top_k_songs_indexes]
        
        logging.info(f"Top {k} recommendations generated successfully.")
        return top_k_songs[['name', 'artist', 'spotify_preview_url']].reset_index(drop=True)
    except Exception as e:
        logging.error(f"Error in recommend: {e}", exc_info=True)
        return None

def main():
    """
    Main function to run the content filtering pipeline.
    """
    try:
        logging.info("Starting pipeline content based filtering...")
        cleaned_data = pd.read_csv("data/cleaned_data.csv")
        df_content_similarity = data_for_content_filtering(cleaned_data)

        train_transformer(
            df_content_similarity,
            frequency_encode_cols=["year"],
            ohe_cols=["artist", "time_signature", "key"],
            tfidf_col="tags",
            standard_scale_cols=["duration_ms", "loudness", "tempo"],
            min_max_scale_cols=["danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence"]
        )

        transformed_data = transform_data(df_content_similarity)
        save_transformed_data(transformed_data, "data/transformed_data.npz")
        top_ten_songs = recommend("Whenever, Wherever", cleaned_data, transformed_data, k=10)

        if top_ten_songs is not None:
            print(top_ten_songs)
        else:
            logging.warning("No recommendations generated.")
    except Exception as e:
        logging.error(f"Error in main: {e}", exc_info=True)

if __name__ == "__main__":
    main()
