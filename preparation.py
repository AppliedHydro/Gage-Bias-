# -------------------------------------------------------------------------------------------------------------------#
# preparation.py
#
# author: Steven Schmitz
#         stevenschmitz@u.boisestate.edu
#
# The following code is used to import and prepare the datasets used for the placement analysis and then combine
# into a single final dataset to be loaded into Placement_analysis.R. Note that in order to execute successfully,
# the following first steps must be taken:
#       i) input catalog subsetting parameters (column name, target value) line XXXXXX
#       ii)
#

import lib_loader as ll  # all necessary libraries are loaded from lib_loader.py
warnings, pd, gpd, Point = ll.setup()

wrk_dir = 'H:/gage_bias_master/'  # working directory
cat_dir = wrk_dir + 'Streamflow_Catalog.csv'  # Streamflow catalog csv file
column_file = wrk_dir + 'subset_options.xlsx'  # Excel spreadsheet with callable columns
file_final = wrk_dir + 'Final_data.csv'  # Output file name
GRADES = wrk_dir + 'GRADES/pfaf_07_riv_3sMERIT_PNW.shp'  # GRADES PNW shapefile
ecoregions = wrk_dir + 'Eco/region_boundaries_FINAL.shp'  # Ecoregions shapefile
attr = wrk_dir + 'HydroATLAS/HydroATLAS_final.csv'  # HydroATLAS attributes file

# key:value pairs to convert ecoregion strings into integer values
eco_val = {'nan': 1, 'Blue Mountains': 1, 'Northern Basin and Range': 2, 'Eastern Cascades Slopes and Foothills': 3,
               'Cascades': 4, 'Klamath Mountains/California High North Coast Range': 5, 'Northern Rockies': 6,
               'Strait of Georgia/Puget Lowland': 7, 'North Cascades': 8, 'Columbia Plateau': 9,
               'Coast Range': 10, 'Idaho Batholith': 11, 'Willamette Valley': 12, 'Middle Rockies': 13,
               'Snake River Plain': 14}

df = pd.read_csv(cat_dir)

def master_subset(column_name, target_value, catalog_path, output_path):
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


def eco_to_int(data):
    '''
    Converts the ecoregion string values in the original catalog format into integer values
    :param data: local address to streamflow catalog
    '''
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(data)
    eco_col = 'ecoregion'
    df[eco_col] = df[eco_col].replace(eco_val)
    # convert floats to integers, ignoring NaN values
    df[eco_col] = pd.to_numeric(df[eco_col], errors='coerce').astype('Int64')
    df.to_csv(data, index=False)
    del df

def eco_to_int_shape(data):
    '''
    Converts the ecoregion string values in the GRADES shapefile into integer values
    :param data: local address to streamflow catalog
    '''
    # Read the CSV file into a pandas DataFrame
    df = gpd.read_file(data)
    eco_col = 'ecoregion'
    df[eco_col] = df[eco_col].str.extract(r'(\d+)', expand=False) # extract integers
    # convert floats to integers, ignoring NaN values
    df[eco_col] = pd.to_numeric(df[eco_col], errors='coerce').astype('Int64')
    df.to_file(wrk_dir + 'GRADES/grades_seg_merge.shp', index=False)
    del df


if __name__ == '__main__':
    print('Refer to {} for column_name and target_value options to filter the'
          ' gages. File output will be the Streamflow catalog subset to'
          ' including only gages that match the target value.'.format(column_file))
    master_subset('status', 'active', cat_dir, file_final)
    eco_to_int(file_final)

# ---------------------------------------------------------------------------#
# spatially joining GRADES river segments with ecoregion data
# ---------------------------------------------------------------------------#

print('Reading GRADES segments...')
grades = gpd.read_file(GRADES)
ecoreg = gpd.read_file(ecoregions)
print('Merging GRADES with ecoregions...')
joined_gdf = gpd.sjoin(grades, ecoreg, how='left', op='intersects')
joined_gdf = joined_gdf.rename(columns={'L3_KEY': 'ecoregion'})
joined_gdf.to_file(wrk_dir + 'GRADES/grades_seg_merge.shp')
del joined_gdf
print('Merge Successful')
eco_to_int_shape(wrk_dir + 'GRADES/grades_seg_merge.shp')


# ---------------------------------------------------------------------------#
# spatially joining GRADES river segments with gage dataset
# ---------------------------------------------------------------------------#

def find_nearest_river(dfpp, dfll, buffersize):
    poly = dfpp.buffer(buffersize)
    polygpd = gpd.GeoDataFrame(dfpp[['Gage_No', 'long', 'lat']], geometry=poly)
    polygpd.crs = 'EPSG:4326'

    # Spatial join
    join = gpd.sjoin(polygpd, dfll, how='left', op='intersects')
    join['geometry_point'] = [Point(lon, lat) for lon, lat in zip(join['long'], join['lat'])]

    # Calculate distance
    join['distance'] = join.apply(
        lambda row: row['geometry_point'].distance(row['geometry']) if row['geometry'] else None, axis=1)

    # Find the nearest point for each COMID
    join11 = join.groupby(['COMID']).agg(
        {'distance': 'min', 'Gage_No': 'first', 'lat': 'first', 'long': 'first'}).reset_index()

    # Merge with dfll to get additional variables
    final = join11.merge(dfll, on='COMID', how='right')[['Gage_No', 'COMID', 'distance', 'lat', 'long', 'ecoregion']]
    return final


if __name__ == '__main__':
    df = pd.read_csv(cat_dir)[['Gage_No', 'lat', 'long']]
    points = [Point(df.long[j], df.lat[j]) for j in range(len(df))]
    dfpp = gpd.GeoDataFrame(df, geometry=points)

    buffersize = 0.035
    allpoints = []

    print('intersecting Streamflow dataset with Grades...')
    dfll = gpd.read_file(wrk_dir + 'GRADES/grades_seg_merge.shp')

    allpoints.append(find_nearest_river(dfpp, dfll, buffersize))
    allpoints = pd.concat(allpoints)

    end_dir = wrk_dir + 'GRADES/GRADES_merge.csv'
    print('writing to %s ...' % end_dir)
    allpoints.to_csv(end_dir, index=False)


# ---------------------------------------------------------------------------#
# spatially joining GRADES/gage dataset with HydroATLAS
# ---------------------------------------------------------------------------#

def Data_final(attr, gages):
    df_A, df_B = pd.read_csv(attr), pd.read_csv(gages)
    assert not df_A.empty, "{} is empty. Reload.".format(attr)
    assert not df_B.empty, "{} is empty. Reload.".format(gages)

    # merge the DataFrames based on COMID
    print('Merging GRADES/gage dataset with HydroATLAS attributes...')
    merged_df = pd.merge(df_A, df_B[['COMID', 'Gage_No', 'lat', 'long', 'ecoregion']], on='COMID', how='left')
    # save the merged DataFrame to a new CSV file
    merged_df.to_csv(file_final, index=False)
    del merged_df  # release memory
    # read the .csv file and set 'COMID' as the index
    df = pd.read_csv(file_final)
    df.set_index('COMID', inplace=True)

    # check for duplicate rows based on 'COMID' index
    duplicate_rows = df[df.index.duplicated(keep='first')]
    # remove duplicate rows, keeping only the first instance
    df = df[~df.index.duplicated(keep='first')]
    return df


if __name__ == '__main__':
    df = Data_final(attr, wrk_dir + 'GRADES/GRADES_merge.csv')
    df.reset_index().to_csv(file_final, index=False)
    print('Final data file saved to {}'.format(wrk_dir))
