# Use the official Python base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy data files
COPY ./data/ /app/data/

# Copy Python scripts
COPY app.py \
     collaberative_filtering.py \
     content_based_filtering.py \
     hybrid_recomender.py \
     utility_required_hybridrec.py \
     data_cleaning.py \
     ./

# Generate self-signed SSL certificates INSIDE the container
RUN mkdir -p /app/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout /app/ssl/key.pem \
      -out /app/ssl/cert.pem \
      -subj "/C=US/ST=State/L=City/O=Org/CN=localhost"

# Expose port 8000 for HTTPS
EXPOSE 8000

# Run Streamlit with HTTPS and WebSocket support
CMD ["streamlit", "run", "app.py", \
      "--server.port", "8000", \
      "--server.address", "0.0.0.0", \
      "--server.sslCertFile", "/app/ssl/cert.pem", \
      "--server.sslKeyFile", "/app/ssl/key.pem", \
      "--server.enableWebsocketCompression", "true"]