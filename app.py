from flask import Flask, request, jsonify
import os
import geopandas as gpd
import time
from shapely.geometry import Point

app = Flask(__name__)

# Define the directory paths for h1 and h2
directory_paths = ["/h_data/h2", "/h_data/h1"]

@app.route('/get_info', methods=['GET'])
def get_info():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    result = []
    available_directories = []

    # Iterate through both directories
    for directory_path in directory_paths:
        if os.path.exists(directory_path):
            available_directories.append(directory_path)
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

                    # If an administrative unit is found, extract the attributes and add them to the result
                    if not admin_unit.empty:
                        attrs = admin_unit.iloc[0].to_dict()
                        result.append(attrs)

    accessible_directories = [dirpath for dirpath in directory_paths if os.path.exists(dirpath)]

    response = {"result": result, "available_directories": accessible_directories}

    if result:
        return jsonify(response)
    else:
        return jsonify({"message": "No administrative units found for the given coordinates.", "available_directories": available_directories}), 404



@app.route('/get_infos', methods=['GET'])
def get_infos():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    result = []

    # Get the content of the current directory (container's working directory)
    current_directory = os.getcwd()

    # Use os.walk to traverse the directory tree
    for root, dirs, files in os.walk(current_directory):
        for file in files:
            if file.endswith(".shp"):
                shp_path = os.path.join(root, file)

                # Load the Shapefile into a GeoDataFrame
                gdf = gpd.read_file(shp_path)

                # Create a shapely Point object from the lat/lon coordinates
                point = Point(lon, lat)

                # Record the start time for query execution
                start_time = time.time()

                # Use the GeoDataFrame's "contains" method to find the administrative units that contain the point
                admin_units = gdf[gdf.geometry.contains(point)]

                # Record the end time for query execution
                end_time = time.time()
                query_time = end_time - start_time

                # Iterate through all the found administrative units and extract attributes
                for _, admin_unit in admin_units.iterrows():
                    attrs = admin_unit.to_dict()
                    # Append the keys and values (excluding "geometry") to the result list
                    keys_values = {key: value for key, value in attrs.items() if key != "geometry"}
                    # Include the filename where the data is found from
                    keys_values["filename"] = file
                    # Include the query time in seconds
                    keys_values["query_time"] = query_time
                    result.append(keys_values)

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
