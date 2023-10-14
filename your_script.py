import os
import geopandas as gpd
from shapely.geometry import Point

# set the path to the Shapefile
shp_path = "/app/h_data/h1/hermes_NPL_everest_0.shp"



# set the coordinate you want to query
lat = 27.7172
lon = 85.3240

# load the Shapefile into a GeoDataFrame
gdf = gpd.read_file(shp_path)

# create a shapely Point object from the lat/lon coordinates
point = Point(lon, lat)

# use the GeoDataFrame's "contains" method to find the administrative unit that contains the point
admin_unit = gdf[gdf.geometry.contains(point)]


if not admin_unit.empty:
    attrs = admin_unit.iloc[0].to_dict()
    for key, value in attrs.items():
        print(f"{key}")
else:
    print("No administrative unit found for the given coordinates.")

# extract the attributes for the administrative unit and print them
# attrs = admin_unit.iloc[0].to_dict()
# print(attrs)