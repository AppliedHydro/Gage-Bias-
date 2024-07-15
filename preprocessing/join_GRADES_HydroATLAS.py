# Assessing placement bias of the global river gauge network
# Nature Sustainability
# Authors: Corey A. Krabbenhoft, George H. Allen, Peirong Lin, Sarah E. Godsey, Daniel C. Allen, Ryan M. Burrows, Amanda G. DelVecchia, Ken M. Fritz, Margaret Shanafield
# Amy J. Burgin, Margaret Zimmer, Thibault Datry, Walter K. Dodds, C. Nathan Jones, Meryl C. Mims, Catherin Franklin, John C. Hammond, Samuel C. Zipper, Adam S. Ward,
# Katie H. Costigan, Hylke E. Beck, and Julian D. Olden

# Date: 2/7/2022

# This code reads GRADES river segments, HydroATLAS river segments, and uses the middle point of all river segments in GRADES
# to spatially join with HydroATLAS river segments
# the joined table of GRADES river ID (COMID) and HydroATLAS river ID (REACH_ID) are then used to extract river attributes


# required library
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import fiona


grades_seg = 'H:/GRADES/MERIT_Basins_v0.7_PNW/pfaf_07_riv_3sMERIT_PNW.shp'
wrk_dir = 'H:/GRADES/'
def findMidPoint():
    '''
    This function reads all GRADES river segments and finds their middle points
    GRADES river segment downloadable from http://hydrology.princeton.edu/data/mpan/MERIT_Basins/MERIT_Hydro_v07_Basins_v01/pfaf_level_01/
    returns mid points shapefile and saves it as a separate file
    '''

    print('importing....')
    # data location for river segment shapefile
    df = gpd.read_file(grades_seg)
    print('imported')

    midpoints = df['geometry'].apply(lambda x: Point(x.interpolate(0.5, normalized=True)))

    # Create a new GeoDataFrame with the midpoints
    data = gpd.GeoDataFrame({'COMID': df['COMID'], 'geometry': midpoints}, crs=df.crs)

    # save middle point shapefile
    data.to_file(wrk_dir + 'GRADES_midpoint.shp')
    print('midpoints saved...')

    return data


def read_HydroATLAS():
    '''
    This function reads all HydroATLAS river segments
    RiverATLAS downloadable from https://figshare.com/articles/dataset/Mapping_the_world_s_free-flowing_rivers_data_set_and_technical_documentation/7688801
    returns as shapefile
    '''
    print('reading HydroATLAS...')

    layers = fiona.listlayers('C:/Users/stevenschmitz/Desktop/PlacementBias/Outputs/HydroATLAS_spatialjoin.shp')
    layer = layers[0]
    llgpd = gpd.read_file('C:/Users/stevenschmitz/Desktop/PlacementBias/Outputs/HydroATLAS_spatialjoin.shp', layer=layer)[
        ['REACH_ID', 'RIV_ORD', 'DOR', 'geometry']]
    print('read...')
    print(len(llgpd))
    # llgpd = llgpd[llgpd['RIV_ORD']>=2] #reduce data size as GRADES channelization threshold is 25km2
    # print(len(llgpd))

    return llgpd


def spatial_join(df, llgpd, buffersize):
    '''
    This function spatially joins the GRADES middle points with HydroATLAS river segments
    Inputs: df (mid point shapefile of GRADES), llgpd (HydroATLAS line shapefile), buffersize (in decimal degree)
    returns the join table
    '''

    print('starting spatial join')
    # create a bufferzone for mid points
    df['lat'] = df['geometry'].y
    df['lon'] = df['geometry'].x
    poly = df.buffer(buffersize)
    polygpd = gpd.GeoDataFrame(df[['COMID', 'lat', 'lon']], geometry=poly)

    # spatial join (make use of geopandas library)
    polygpd.crs = llgpd.crs
    print('... spatial join with flowlines.. wait ...')
    join = gpd.sjoin(polygpd, llgpd, how='inner', op='intersects')

    merge = join.merge(llgpd[['REACH_ID', 'geometry']], on=['REACH_ID'])
    del join  # release memory
    merge['distance'] = [Point(merge['lon'][i], merge['lat'][i]).distance(merge['geometry_y'][i]) for i in
                         range(0, len(merge))]
    print(len(merge))
    join11 = merge.groupby(['COMID']).agg({'distance': 'min'})
    print(len(join11))
    merge11 = join11.merge(merge, on=['COMID', 'distance'], how='inner')
    del merge, join11  # release memory
    final = merge11[['COMID', 'REACH_ID', 'DOR', 'distance']]  # no need to retain geometry
    del merge11  # release memory

    final = final.drop_duplicates(subset='COMID')
    final.REACH_ID = final.REACH_ID.astype('int64')

    return final


if __name__ == '__main__':
    # find river segment middle points for GRADES
    df = findMidPoint()

    # read HydroATLAS river segments
    llgpd = read_HydroATLAS()

    # spatially join GRADES with HydroATLAS
    dfjoin = spatial_join(df, llgpd, 0.05)

    # save join table as csv file
    print('saving file...')
    fon = wrk_dir + 'GRADES_Hydro_Join.csv'
    print('... writing to %s ...' % fon)
    dfjoin.to_csv(fon, index=False)