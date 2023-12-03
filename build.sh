#!/bin/bash

# Define variables
IMAGE_NAME="flask-test"  # Replace with your image name
REPO="ajaysurapaneni/flask-test"       # Replace with your Docker repository (e.g., username/repo)
TAG="latest"                  # You can use a specific tag like "v1.0"

DOCKER_USERNAME="ajaysurapaneni"
DOCKER_PASSWORD="project461"
# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Tag the image for the repository
echo "Tagging Docker image..."
docker tag $IMAGE_NAME $REPO:$TAG

# Log in to Docker Hub
echo "Logging in to Docker Hub..."
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

# Push the image to the repository
echo "Pushing image to Docker repository..."
docker push $REPO:$TAG

echo "Build and push completed."
