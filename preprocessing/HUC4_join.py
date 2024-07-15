import geopandas as gpd
from shapely.geometry import Point

csv_file = "H:/Catalog_Subsets/Catalog_Final.csv"
shapefile = "C:/Users/stevenschmitz/Desktop/Esri Shapefiles/Layers/HUC4.shp"
output_file = "H:/Catalog_Subsets/Catalog_Final_Merge.shp"

# Read huc4's into a DataFrame
csv_df = gpd.read_file(csv_file)

# Convert DataFrame to GeoDataFrame with point geometries
geometry = [Point(xy) for xy in zip(csv_df['long'], csv_df['lat'])]
csv_gdf = gpd.GeoDataFrame(csv_df, geometry=geometry)
shapefile_gdf = gpd.read_file(shapefile)
shapefile_gdf = shapefile_gdf.rename(columns={'huc4': 'huc4_shapefile'})
joined_gdf = gpd.sjoin(csv_gdf, shapefile_gdf, how="left", op="within")

# Drop the duplicate geometry column from the CSV GeoDataFrame
joined_gdf.drop(columns='geometry', inplace=True)
print(joined_gdf)
joined_gdf.to_file(output_file)
