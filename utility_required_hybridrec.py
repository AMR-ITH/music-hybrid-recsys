import pandas as pd
import joblib
from scipy.sparse import csr_matrix
from scipy.sparse import save_npz
from pathlib import Path

def main():
    # Load user listened data
    data_path = Path("data/filtered_songs.csv")
    user_listened_data = pd.read_csv(data_path)
    
    # Convert track_id to category type
    user_listened_data["track_id"] = user_listened_data["track_id"].astype("category")
    
    # Drop unnecessary columns
    user_listened_data.drop(columns=["track_id", "name", "spotify_preview_url"], errors="ignore", inplace=True)
    
    # Load the transformer
    current_dir = Path().cwd()
    transformer_path = current_dir / "transformer.joblib"
    transformer = joblib.load(transformer_path)
    
    # Transform the data
    transformed_data = transformer.transform(user_listened_data)
    transformed_data = csr_matrix(transformed_data)
    print(f"Transformed data shape: {transformed_data.shape}")
    
    # Save the transformed data
    save_path = current_dir / "data" / "content_based.npz"
    save_npz(save_path, transformed_data)

if __name__ == "__main__":
    main()

    
