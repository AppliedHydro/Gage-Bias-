import geopandas as gpd
from shapely.geometry import Point

# File paths
csv_file = "H:/Catalog_Subsets/Catalog_Final.csv"
shapefile = "C:/Users/stevenschmitz/Desktop/Esri Shapefiles/Layers/HUC4.shp"

# Read CSV into a DataFrame
csv_df = gpd.read_file(csv_file)

# Convert DataFrame to GeoDataFrame with Point geometries
geometry = [Point(xy) for xy in zip(csv_df['long'], csv_df['lat'])]
csv_gdf = gpd.GeoDataFrame(csv_df, geometry=geometry)

# Read shapefile into a GeoDataFrame
shapefile_gdf = gpd.read_file(shapefile)

# Rename columns in the shapefile to avoid suffixes
shapefile_gdf = shapefile_gdf.rename(columns={'huc4': 'huc4_shapefile'})

# Perform spatial join (one-to-many)
joined_gdf = gpd.sjoin(csv_gdf, shapefile_gdf, how="left", op="within")

# Drop the duplicate geometry column from the CSV GeoDataFrame
joined_gdf.drop(columns='geometry', inplace=True)

# Print or save the result
print(joined_gdf)

# Save the result to a new shapefile or CSV if needed
output_file = "H:/Catalog_Subsets/Catalog_Final_Merge.shp"
joined_gdf.to_file(output_file)
