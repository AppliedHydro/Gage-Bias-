# join_gauge_GRADES.py
#
# Author: Steven Schmitz
# date: 11.12.2023
# Modified for Streamflow Catalog Gage Placement Analysis Project from original file below
# Source: https://github.com/dry-rivers-rcn/G4
#
# Assessing placement bias of the global river gauge network
# Nature Sustainability
# Authors: Corey A. Krabbenhoft, George H. Allen, Peirong Lin, Sarah E. Godsey, Daniel C. Allen, Ryan M. Burrows, Amanda G. DelVecchia, Ken M. Fritz, Margaret Shanafield
# Amy J. Burgin, Margaret Zimmer, Thibault Datry, Walter K. Dodds, C. Nathan Jones, Meryl C. Mims, Catherin Franklin, John C. Hammond, Samuel C. Zipper, Adam S. Ward,
# Katie H. Costigan, Hylke E. Beck, and Julian D. Olden

# Date: 2/7/2022

# This code all gauge locations, and spatially joins them with GRADES river segments
# output is the joined table of gauge ID (stationid) with GRADES river ID (COMID)

# required library
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

catalog = 'H:/Final_data.csv'
wrk_dir = 'H:/GRADES/'
grades_seg = 'H:/GRADES/GRADES_eco.shp'


def find_nearest_river(dfpp, dfll, buffersize):
    poly = dfpp.buffer(buffersize)
    polygpd = gpd.GeoDataFrame(dfpp[['Gage_No', 'long', 'lat']], geometry=poly)
    polygpd.crs = 'EPSG:4326'

    # Spatial join
    join = gpd.sjoin(polygpd, dfll, how='left', op='intersects')

    # Create a 'geometry_point' column for points
    join['geometry_point'] = [Point(lon, lat) for lon, lat in zip(join['long'], join['lat'])]

    # Calculate distance
    join['distance'] = join.apply(lambda row: row['geometry_point'].distance(row['geometry']) if row['geometry'] else None, axis=1)

    # Find the nearest point for each COMID
    join11 = join.groupby(['COMID']).agg({'distance': 'min', 'Gage_No': 'first', 'lat': 'first', 'long': 'first'}).reset_index()

    # Merge with dfll to get additional variables
    final = join11.merge(dfll, on='COMID', how='right')[['Gage_No', 'COMID', 'distance', 'lat', 'long', 'ecoregion']]

    return final

if __name__ == '__main__':
    df = pd.read_csv(catalog)[['Gage_No', 'lat', 'long']]
    points = [Point(df.long[j], df.lat[j]) for j in range(len(df))]
    dfpp = gpd.GeoDataFrame(df, geometry=points)

    buffersize = 0.035
    allpoints = []

    print('... intersecting with Grades')
    dfll = gpd.read_file(grades_seg)

    allpoints.append(find_nearest_river(dfpp, dfll, buffersize))
    allpoints = pd.concat(allpoints)

    end_dir = wrk_dir + 'GRADES_test.csv'
    print('... writing to %s ...' % end_dir)
    allpoints.to_csv(end_dir, index=False)
