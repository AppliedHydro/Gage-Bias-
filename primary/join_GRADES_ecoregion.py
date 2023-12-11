#join_GRADES_ecoregion.py
#
#Author: Steven Schmitz
#date: 12.01.2023
#
#spatially joins ecoregion values in the pacific northwest to GRADES river segments
#to be used bias variable in final dataset.

import geopandas as gpd

GRADES = 'H:/GRADES/MERIT_Basins_v0.7_PNW/pfaf_07_riv_3sMERIT_PNW.shp'
ecoregions = 'H:/Misc/ecoregion_shapefile/eco-region shapefile/region_boundaries_FINAL.shp'
output_path = 'H:/GRADES/GRADES_eco.shp'

GRADES = gpd.read_file(GRADES)
ecoregions = gpd.read_file(ecoregions)
joined_gdf = gpd.sjoin(GRADES, ecoregions, how='left', op='intersects')
joined_gdf = joined_gdf.rename(columns={'L3_KEY': 'ecoregion'})
print(joined_gdf.columns)
joined_gdf.to_file(output_path, driver='ESRI Shapefile')
