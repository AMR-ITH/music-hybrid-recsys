#!/bin/bash
# Log everything to start_docker.log
exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging in to ECR..."
aws aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 116981799876.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling Docker image..."
docker pull 116981799876.dkr.ecr.ap-south-1.amazonaws.com/spotify_recsys:latest

echo "Checking for existing container..."
if [ "$(docker ps -q -f name=hybrid_recsys)" ]; then
    echo "Stopping existing container..."
    docker stop hybrid_recsys
fi

if [ "$(docker ps -aq -f name=hybrid_recsys)" ]; then
    echo "Removing existing container..."
    docker rm hybrid_recsys
fi


echo "Starting new container..."
docker run -d --memory=512m --memory-swap=1g -p 8000:8000 --name hybrid_recsys 116981799876.dkr.ecr.ap-south-1.amazonaws.com/spotify_recsys:latest

echo "Container started successfully."