# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to your project directory
WORKDIR /app

# Install GDAL
RUN apt-get update && apt-get install -y  build-essential libgdal-dev

# Set GDAL_CONFIG environment variable
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt

RUN pip install -r requirements.txt
EXPOSE 5000
# Run the script when the container launches
CMD ["python", "app.py"]
