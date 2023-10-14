

# Geospatial Data Query API

## Overview

The Geospatial Data Query API is a Flask-based server that allows you to query geospatial data stored in shapefiles using latitude and longitude coordinates. This API provides a simple way to find administrative units that contain a specific geographical point.

## Features

- Query geospatial data by providing latitude and longitude coordinates.
- Retrieve attributes of administrative units that contain the specified point.
- **Debug**:  List the available directories and files in the server's working directory.

## Getting Started

Follow these steps to set up and use the Geospatial Data Query API:

### Building the Docker Image

1. Clone this repository to your local machine.
2. In your terminal, navigate to the project's root directory.
3. Build the Docker image using the following command:

   ```
   docker build -t script-container .
   ```

### Running the Server

To run the server, use the following command:

```
docker run -it -p 5000:5000 -v "$(pwd)":/app script-container
```

This command maps the port 5000 of the container to your local machine's port, allowing you to access the API via a web browser.

### Accessing the API

The API can be accessed through a web browser or via HTTP requests. Here's an example request URL:

```
http://localhost:5000/get_info?lat=27.7172&lon=85.3240
```

Replace the `lat` and `lon` query parameters with your desired latitude and longitude coordinates.

## API Endpoints

- `/get_info`: This endpoint accepts GET requests with `lat` and `lon` query parameters and returns information about the administrative units containing the specified coordinates.
- `/get_info_walk`: This endpoint provides the same functionality as `/get_info`, but it uses the "walk" approach to query geospatial data. Here the application walks through directories and subdirectories to find shapefiles and extract data

## Additional Functionality

The API can also list the contents of the current directory by sending a GET request to `/get_directory_list`.

## Dependencies

- Flask: A lightweight Python web framework.
- Geopandas: A library for working with geospatial data.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is yet to be licensed under the MIT License.

