# kerstlan_voting_app

# Set your email password
export EMAIL_PASSWORD=<your_email_password>

# Build the Docker image
docker build -t kerstlan-voting-app .

# Run the Docker container
docker run -p 8501:8501 -e EMAIL_PASSWORD -it -v $(pwd)/config/:/app/config/ kerstlan-voting-app