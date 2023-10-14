from flask import Flask, request, jsonify
import os
import geopandas as gpd
import time
import requests
from shapely.geometry import Point

app = Flask(__name__)

# Define the directory paths for h1 and h2
directory_paths = ["/app/h_data/h2", "/app/h_data/h1","/app/h_data/h3"]


import os

def load_shapefiles(lat, lon, approach="default"):
    start_time = time.time()
    result = []

    if approach == "walk":
        for directory_path in directory_paths:
            if os.path.exists(directory_path):
                for root, _, files in os.walk(directory_path):
                    print(f"Processing directory: {directory_path}")
                    for shp_filename in files:
                         if shp_filename.lower().endswith(".shp"):
                            shp_path = os.path.join(root, shp_filename)
                            print(f"Processing file: {shp_path}")
                            gdf = gpd.read_file(shp_path)
                            point = Point(lon, lat)
                            admin_unit = gdf[gdf.geometry.contains(point)]

                            end_time = time.time()
                            query_time = end_time - start_time

                            for _, admin_unit in admin_unit.iterrows():
                                attrs = admin_unit.to_dict()
                                keys_values = {key: value for key, value in attrs.items() if key != "geometry"}
                                keys_values["filename"] = shp_path
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

                                keys_values["formattedString"] = ", ".join(formatted_string)
                                keys_values["query_time"] = query_time

                                result.append(keys_values)
    else:
        for directory_path in directory_paths:
            if os.path.exists(directory_path):
                if directory_path == "/app/h_data/h2":
                    pattern = "new_wgs"
                elif directory_path == "/app/h_data/h1":
                    pattern = "everest"
                else:
                    continue

                for i in range(1):
                    shp_filename = f"hermes_NPL_{pattern}_3.shp"
                    shp_path = os.path.join(directory_path, shp_filename)

                    if os.path.exists(shp_path):
                        gdf = gpd.read_file(shp_path)
                        point = Point(lon, lat)
                        admin_unit = gdf[gdf.geometry.contains(point)]

                        end_time = time.time()
                        query_time = end_time - start_time

                        for _, admin_unit in admin_unit.iterrows():
                            attrs = admin_unit.to_dict()
                            keys_values = {key: value for key, value in attrs.items() if key != "geometry"}
                            keys_values["filename"] = shp_path
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

                            keys_values["formattedString"] = ", ".join(formatted_string)
                            keys_values["query_time"] = query_time

                            result.append(keys_values)

    return result

@app.route('/get_info', methods=['GET'])
def get_info():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    result = load_shapefiles(lat, lon, approach="default")

    if result:
        return jsonify({"result":result})
    else:
        return jsonify({"message": "No administrative units found for the given coordinates."}), 404


@app.route('/get_info_walk', methods=['GET'])
def get_info_walk():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    result = load_shapefiles(lat, lon, approach="walk")

    if result:
       return jsonify({"result":result})
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
