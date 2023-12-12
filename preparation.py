#-------------------------------------------------------------------------------------------------------------------#
# preparation.py
#
# author: Steven Schmitz
#         stevenschmitz@u.boisestate.edu
#
# The following code is used to import and prepare the datasets used for the placement analysis and then combine 
# into a single final dataset to be loaded into Placement_analysis.R. Note that in order to execute successfully,
# the following first steps must be taken:
#       i) edit file directories (line x -
#       ii) edit output file names (line x -
#   

import lib_loader as ll # all necessary libraries are loaded from lib_loader.py
ll.setup()

wrk_dir = 'H:/Catalog_Subsets/'                # working directory
cat_dir = wrk_dir + 'Streamflow_Catalog.csv'   # Streamflow catalog csv file
column_file = 'H:/subset_options.xlsx'         # Excel spreadsheet with callable columns
file_final = 'XXXX.csv'                        # Output file name

df = pd.read_csv(cat_dir)

def master_subset(column_name, target_value,catalog_path, output_path):
    '''
    Master subsetting function, saves filtered catalog to output file path to be used
    for placement analysis.
    :param catalog_path: directory of streamflow catalog in .csv format
    :param column_name: name of catalog column that target_value is coming from
    :param target_value: value used for filtering the catalog
    :param output_path: save location for filtered catalog as csv
    :return: pd.DataFrame of filtered catalog
    '''
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=pd.errors.DtypeWarning)
            df = pd.read_csv(catalog_path)
            if column_name == 'huc4':
                target_value = int(target_value)
            filtered_df = df[df[column_name] == target_value]
            assert not filtered_df.empty, "No matching rows found."
            filtered_df.to_csv(output_path, index=False)
            print(f"Rows with '{target_value}' saved to {output_path}")
            return filtered_df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    print('Refer to {} for column_name and target_value options to filter the'
          ' gages. File output will be the Streamflow catalog subset to'
          'including only gages that match the target value.'.format(column_file))
    master_subset('status', 'active', cat_dir, wrk_dir + file_final)

#---------------------------------------------------------------------------#
# spatially joining GRADES river segments with ecoregion data
#---------------------------------------------------------------------------#

GRADES = 'H:/GRADES/MERIT_Basins_v0.7_PNW/pfaf_07_riv_3sMERIT_PNW.shp'
ecoregions = 'H:/Misc/ecoregion_shapefile/eco-region shapefile/region_boundaries_FINAL.shp'
output_path = 'H:/GRADES/GRADES_eco.shp'

GRADES = gpd.read_file(GRADES)
ecoregions = gpd.read_file(ecoregions)
joined_gdf = gpd.sjoin(GRADES, ecoregions, how='left', op='intersects')
joined_gdf = joined_gdf.rename(columns={'L3_KEY': 'ecoregion'})
print(joined_gdf.columns)
joined_gdf.to_file(output_path, driver='ESRI Shapefile')

#---------------------------------------------------------------------------#
# spatially joining GRADES river segments with gage dataset
#---------------------------------------------------------------------------#

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
