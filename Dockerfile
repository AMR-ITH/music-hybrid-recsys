# Use slim Python image for smaller size and efficiency
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_app.txt \
    && rm requirements.txt

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

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Expose the port Streamlit will run on
EXPOSE 8000

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--logger.level", "debug"]
