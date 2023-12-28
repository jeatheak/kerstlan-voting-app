# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y install git

# Clone the GitHub repo
RUN git clone https://github.com/jeatheak/kerstlan-voting-app.git .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port streamlit will run on
EXPOSE 8501

# Command to run on container start
# CMD ["/bin/sh"]
CMD ["sh", "-c", "git fetch origin main && git pull origin main && streamlit run app.py"]
