# This code takes all gauge locations, and spatially joins them with GRADES river segments
# output is the joined table of gauge ID (stationid) with GRADES river ID (COMID)

# required library
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

wrk_dir = 'H:/GRADES/'

def find_nearest_river(dfpp, dfll, buffersize):
    '''
    This function finds the nearest river reach ID for each gauge
    input: dfpp: point shapefile of the gauges; dfll: line shapefile of GRADES
    '''
    # create buffer
    print('   create buffer... wait ...')
    poly = dfpp.buffer(buffersize)
    polygpd = gpd.GeoDataFrame(dfpp[['Gage_No', 'long', 'lat']], geometry=poly)
    polygpd.crs = 'EPSG:4326'
    # spatial join
    print('   spatial join with flowlines.. wait ...')
    join = gpd.sjoin(polygpd, dfll, how='inner', op='intersects')
    merge = join.merge(dfll, on='COMID', how='left')
    print('   calculating distance.. wait ...')
    merge['distance'] = [Point(merge['long'][i], merge['lat'][i]).distance(merge['geometry_y'][i]) for i in
                         range(0, len(merge))]
    join11 = merge.groupby(['Gage_No']).agg({'distance': 'min'}).reset_index()  # min dist: width and MERIT
    merge11 = join11.merge(merge, on=['Gage_No', 'distance'], how='left')
    final = merge11[['Gage_No', 'COMID', 'distance', 'long', 'lat']]

    return final


if __name__ == '__main__':
    # Choose specific subset of gages from destination folder
    catalog = 'H:/Catalog_Subsets/Discrete_cat.csv'
    df = pd.read_csv(catalog)[['Gage_No', 'lat', 'long']]
    points = [Point(df.long[j], df.lat[j]) for j in range(len(df))]

    # create GeoDataFrame
    dfpp = gpd.GeoDataFrame(df, geometry=points)

    # read GRADES river segments and perform spatial join
    buffersize = 0.05  # ~5km
    allpoints = []

    # GRADES river segment downloadable from http://hydrology.princeton.edu/data/mpan/MERIT_Basins/MERIT_Hydro_v07_Basins_v01/pfaf_level_01/
    grades_seg = 'H:/GRADES/MERIT_Basins_v0.7_PNW/pfaf_07_riv_3sMERIT_PNW.shp'
    print('... intersecting with Grades')
    dfll = gpd.read_file(grades_seg)
    allpoints.append(find_nearest_river(dfpp, dfll, buffersize))
    allpoints = pd.concat(allpoints)

    # save to file
    end_dir = wrk_dir + 'GRADES_gage_discrete.csv'
    print('... writing to %s ...' % end_dir)
    allpoints.to_csv(end_dir, index=False)
