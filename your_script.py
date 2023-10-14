import os
import geopandas as gpd
from shapely.geometry import Point

# Define the directory paths for h1 and h2
directory_paths = ["/app/h_data/h2", "/app/h_data/h1"]

# Set the coordinates you want to query
lat = 27.7172
lon = 85.3240

# Iterate through both directories
for directory_path in directory_paths:
    print(f"Processing directory: {directory_path}")
    for i in range(4):  # Assuming you have new_wgs_0.shp to new_wgs_3.shp
        if "h2" in directory_path:
            shp_filename = f"hermes_NPL_new_wgs_{i}.shp"
        else:
            shp_filename = f"hermes_NPL_everest_{i}.shp"

        shp_path = os.path.join(directory_path, shp_filename)

        # Load the Shapefile into a GeoDataFrame
        gdf = gpd.read_file(shp_path)

        # Create a shapely Point object from the lat/lon coordinates
        point = Point(lon, lat)

        # Use the GeoDataFrame's "contains" method to find the administrative unit that contains the point
        admin_unit = gdf[gdf.geometry.contains(point)]

        # Print the keys in the attribute table for this shapefile
        if not admin_unit.empty:
            attrs = admin_unit.iloc[0].to_dict()
            print(f"Keys for {shp_filename}:")
            for key, value in attrs.items():
                print(key)
                if key != "geometry":
                    print(value)
        else:
            print(f"No administrative unit found in {shp_filename} for the given coordinates.")
