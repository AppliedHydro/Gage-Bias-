# Hydro_attr_merge.py
#
# Author: Steven Schmitz
# date: 11.12.2023
#
# This script clips the primary HydroATLAS attributes file to the Pacific Northwest - the scope of Streamflow catalog
# gage dataset. It also deletes older streamflow gage information merged into the attribute data and prepares it to be
# updated with new gage data.
# columns removed: see line 54 -> columns_removed

import pandas as pd

wrk_dir = 'H:/'                                                                                                  # working directory
hydro_attr = wrk_dir + 'HydroATLAS/Krabbenhoft_etal_2022_NatSus_Stream_characteristics_data/Attribute_table.csv' # HydroATLAS attribute file
hydro_river = wrk_dir + 'HydroATLAS/HydroATLAS_PNW.csv'                                                          # HydroATLAS river segments clipped to PNW
output_name = 'HydroATLAS_final.csv'                                                                             # Output file name

def Hydro_cleanup(hydro_attr,hydro_river):
    '''
    Reads HydroATLAS attributes and merges with HydroATLAS river segments based off of REACH_ID index. Also cleans out
    duplicates and checks for empty REACH_ID parameters to validate the merge.
    :param hydro_attr: .csv file of HydroATLAS attributes
    :param hydro_river: .csv file of HydroATLAS river segments with REACH_ID and geospatial data
    :return: pd.DataFrame of merged attributes and river segment data
    '''
    # check to confirm that REACH_ID is in the loaded data - used as index for merge with HydroATLAS river segments
    try:
        df1 = pd.read_csv(hydro_attr)
        if 'REACH_ID' not in df1.columns:
            print("Error: REACH_ID column not found in {}".format(hydro_attr))
            exit()
    except FileNotFoundError:
        print("Error: {} not found.".format(hydro_attr[-25:]))
        exit()

    try:
        df2 = pd.read_csv(hydro_river)
        if 'REACH_ID' not in df2.columns:
            print("Error: REACH_ID column not found in {}".format(hydro_river))
            exit()
    except FileNotFoundError:
        print("Error: {} not found.".format(hydro_river[-18:])) #add hydro filename index
        exit()

    # merge the two DataFrames using REACH_ID as the index after removing duplicates from main
    df1 = df1.drop_duplicates(subset=['REACH_ID'], keep='first')
    merged_df = pd.merge(df1, df2, on='REACH_ID', how='inner')

    # check if there are any null values in the REACH_ID column
    if merged_df['REACH_ID'].isnull().any():
        print("Error: Merge failed. Check the REACH_ID column for missing values.")
        exit()

    # check for duplicates in new dataframe
    if merged_df.duplicated(subset='REACH_ID').any():
        print("Duplicates found in the merged DataFrame. Please check your data.")
        exit()

    columns_remove = ['Unnamed: 0','stationid','lat','long','distance','noFlowGauge','continent']
    df_final = merged_df.drop(columns=columns_remove)
    return df_final

if __name__ == '__main__':
    df_final = Hydro_cleanup(hydro_attr,hydro_river)
    df_final.to_csv(wrk_dir + output_name_name, index=False)
