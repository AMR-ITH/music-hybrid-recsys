import pandas as pd
import logging
from pathlib import Path

# Configure logging to log to both file and console
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log_file.log"),  # Logs to file
        logging.StreamHandler()  # Logs to console (debug mode)
    ],
)

def clean_data(music_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the music data by performing the following operations:
    1. Removes duplicate rows based on the columns "spotify_id", "year", and "duration_ms".
    2. Drops the columns "genre" and "spotify_id".
    3. Fills missing values in the "tags" column with the string "no_tags".
    4. Converts the text in the "artist", "tags", and "name" columns to lowercase.

    Parameters:
    music_data (pd.DataFrame): The input DataFrame containing music data.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    logging.debug("Starting data cleaning...")
    
    cleaned_data = (
        music_data
        .drop_duplicates(subset=["spotify_id", "year", "duration_ms"])
        .drop(columns=["genre", "spotify_id"], errors="ignore")
        .fillna({"tags": "no_tags"})
        .assign(
            artist=lambda x: x["artist"].str.lower(),
            tags=lambda x: x["tags"].str.lower(),
            name=lambda x: x["name"].str.lower(),
        )
    )

    logging.info("Data cleaning completed successfully.")
    return cleaned_data



def main():
    """
    Main function to clean music data.

    This function performs the following steps:
    1. Gets the current working directory.
    2. Constructs the path to the "Music Info.csv" file located in the "data" directory.
    3. Reads the music data from the CSV file.
    4. Cleans the music data using the `clean_data` function.
    5. Saves the cleaned data to a new CSV file named "cleaned_data.csv" in the "data" directory.
    """
    try:
        logging.info("Starting data cleaning process file:data_cleaning.py ...")
        current_dir = Path().cwd()
        music_data_path = current_dir / "data" / "Music Info.csv"

        logging.debug(f"Reading music data from {music_data_path}")

        music_data = pd.read_csv(music_data_path)

        cleaned_data = clean_data(music_data)

        cleaned_data_path = current_dir / "data" / "cleaned_data.csv"
        cleaned_data.to_csv(cleaned_data_path, index=False)

        logging.info(f"Cleaned data saved to {cleaned_data_path}")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.exception("An error occurred.")  # Logs the full traceback for debugging

if __name__ == "__main__":
    main()
