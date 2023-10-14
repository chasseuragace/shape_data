from flask import Flask, request, jsonify
import os
import geopandas as gpd
from shapely.geometry import Point

app = Flask(__name__)

# Define the directory paths for h1 and h2
directory_paths = ["/h_data/h2", "/h_data/h1"]

@app.route('/get_info', methods=['GET'])
def get_info():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    result = []

    # Iterate through both directories
    for directory_path in directory_paths:
        for i in range(4):  # Assuming you have new_wgs_0.shp to new_wgs_3.shp
            shp_filename = f"hermes_NPL_new_wgs_{i}.shp"
            shp_filename2 = f"hermes_NPL_everest_{i}.shp"
            shp_path = os.path.join(directory_path, shp_filename)

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

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No administrative units found for the given coordinates."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
