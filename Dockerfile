# set up the base image
FROM python:3.12

# set the working directory
WORKDIR /app/

# copy the requirements file to workdir
COPY requirements.txt .

# install the requirements
RUN pip install -r requirements.txt

# Create .streamlit directory and config file
RUN mkdir -p .streamlit
RUN echo '[server]\nenableCORS = false\nenableXsrfProtection = false' > .streamlit/config.toml

# Copy all required data files at once
COPY ./data/cleaned_data.csv \
     ./data/content_based.npz \
     ./data/item_user_matrix.npz \
     ./data/transformed_data.npz \
     ./data/filtered_songs.csv \
     ./data/

# Copy all required Python scripts at once
COPY app.py \
     collaberative_filtering.py \
     content_based_filtering.py \
     hybrid_recomender.py \
     utility_required_hybridrec.py \
     data_cleaning.py \
     ./

# expose the port on the container
EXPOSE 8000

# run the streamlit app with additional flags
CMD [ "streamlit", "run", "app.py", "--server.port=8000", "--server.enableCORS=false", "--server.enableXsrfProtection=false" ]