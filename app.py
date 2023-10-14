from flask import Flask, request, jsonify
import os
import geopandas as gpd
import time
import requests
from shapely.geometry import Point

app = Flask(__name__)

# Define the directory paths for h1 and h2
directory_paths = ["/app/h_data/h2", "/app/h_data/h1"]


def load_shapefiles(lat, lon, approach="os.walk"):
    # Record the start time for query execution
    start_time = time.time()
    result = []

    # Determine the current directory based on the chosen approach
    if approach == "os.walk":
        current_directory = os.getcwd()
    else:
        current_directory = None  # Set this to the correct directory

    # Iterate through both directories
    for directory_path in directory_paths:
        if os.path.exists(directory_path):
            for i in range(4):  # Assuming you have new_wgs_0.shp to new_wgs_3.shp
                shp_filename = f"hermes_NPL_new_wgs_{i}.shp"
                shp_path = os.path.join(directory_path, shp_filename)

                if os.path.exists(shp_path):
                    # Load the Shapefile into a GeoDataFrame
                    gdf = gpd.read_file(shp_path)

                    # Create a shapely Point object from the lat/lon coordinates
                    point = Point(lon, lat)

                    

                    # Use the GeoDataFrame's "contains" method to find the administrative unit that contains the point
                    admin_unit = gdf[gdf.geometry.contains(point)]

                    # Record the end time for query execution
                    end_time = time.time()
                    query_time = end_time - start_time

                    # Iterate through all the found administrative units and extract attributes
                    for _, admin_unit in admin_unit.iterrows():
                        attrs = admin_unit.to_dict()

                        # Append the keys and values (excluding "geometry") to the result list
                        keys_values = {key: value for key, value in attrs.items() if key != "geometry"}

                        # Include the filename where the data is found from
                        keys_values["filename"] = shp_filename

                        # Create a formattedString based on available attributes
                        formatted_string = []

                        if "PALIKA" in attrs:
                            formatted_string.append(attrs["PALIKA"])
                        if "DISTRICT" in attrs:
                            formatted_string.append(attrs["DISTRICT"])
                        if "PR_NAME" in attrs:
                            formatted_string.append(attrs["PR_NAME"])
                        if "PROVINCE" in attrs and "PR_NAME" not in attrs:
                            formatted_string.append(f"Province {attrs['PROVINCE']}")
                        if "TYPE" in attrs:
                            formatted_string.append(attrs["TYPE"])
                        if "LOCAL" in attrs:
                            formatted_string.append(attrs["LOCAL"])

                        # Construct the final formattedString
                        keys_values["formattedString"] = ", ".join(formatted_string)
                        keys_values["query_time"] = query_time

                        result.append(keys_values)

    return result

@app.route('/get_info', methods=['GET'])
def get_info():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    result = load_shapefiles(lat, lon, approach="os.walk")

    if result:
        return jsonify({"result":result})
    else:
        return jsonify({"message": "No administrative units found for the given coordinates."}), 404


@app.route('/get_info_gpd', methods=['GET'])
def get_info_gpd():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    result = load_shapefiles(lat, lon, approach="gpd")

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No administrative units found for the given coordinates."}), 404

@app.route('/get_directory_list', methods=['GET'])
def get_directory_list():
    result = []
    # Get the content of the current directory (container's working directory)
    current_directory = os.getcwd()
    current_directory_contents = os.listdir(current_directory)

    # Add the current directory's contents to the result
    result.append(f"Contents of current directory ({current_directory}):")
    for item in current_directory_contents:
        result.append(item)

    return jsonify(result)


@app.route('/getmovie')
def get_movie_info():
    # Define the Jikan API URL with the query parameter
    jikan_url = 'https://api.jikan.moe/v4/anime?q=Naruto&sfw'

    try:
        # Send a GET request to the Jikan API
        response = requests.get(jikan_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response from the Jikan API
        movie_info = response.json()

        # Return the movie info as JSON response
        return jsonify(movie_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
