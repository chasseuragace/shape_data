# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to your project directory
WORKDIR /app

# Install GDAL
RUN apt-get update && apt-get install -y libgdal-dev

# Set GDAL_CONFIG environment variable
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org geopandas shapely

# Run the script when the container launches
CMD ["python", "your_script.py"]
