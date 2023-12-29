# Kerstlan Voting App

## Introduction
Welcome to the Kerstlan Voting App! This application allows you to set up and run a voting system with ease.

## Prerequisites
Before you start, make sure you have the following:

- Docker installed on your machine
- Your email password handy for configuration

## Setup
```bash
# Set your email password
export EMAIL_PASSWORD=<your_email_password>

# Build the Docker image
docker build -t kerstlan-voting-app .

# Run the Docker container
docker run -p 8501:8501 -e EMAIL_PASSWORD -it -v $(pwd)/config/:/app/config/ -v $(pwd)/uploads/:/app/uploads/ -v $(pwd)/database/db/:/app/database/db/ kerstlan-voting-app
```

# Configuration

Ensure you customize the necessary configurations in the config/ directory to suit your requirements.
Feedback

# If you encounter any issues or have suggestions, feel free to open an issue or contribute to the project.

Happy voting!