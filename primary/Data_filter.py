# Data_filter.py
#
# Author: Steven Schmitz
# date: 11.01.2023
#
# Merges the final HydroATLAS dataset (attributes and segments) to GRADES and streamflow gage dataset to create
# master. The output can be used directly in the placement_analysis.R code as data input.

import pandas as pd

wrk_dir = 'H:/'                                    # working directory
final_path = 'H:/Final_data.csv'                   # output location + file name for final output
attr = wrk_dir + 'HydroATLAS/HydroATLAS_final.csv' # HydroATLAS attributes file
gages = wrk_dir + 'GRADES/GRADES_test.csv'         # GRADES/Gage merged file

def Data_final(attr,gages):
    df_A, df_B = pd.read_csv(attr),pd.read_csv(gages)
    assert not df_A.empty,"{} is empty. Reload.".format(attr)
    assert not df_B.empty,"{} is empty. Reload.".format(gages)

    # merge the DataFrames based on COMID
    merged_df = pd.merge(df_A, df_B[['COMID', 'Gage_No', 'lat', 'long','ecoregion']], on='COMID', how='left')
    # save the merged DataFrame to a new CSV file
    merged_df.to_csv(wrk_dir + 'Final_data.csv', index=False)
    file_path = wrk_dir + 'Final_data.csv'
    # read the .csv file and set 'COMID' as the index
    df = pd.read_csv(file_path)
    df.set_index('COMID', inplace=True)

    # check for duplicate rows based on 'COMID' index
    duplicate_rows = df[df.index.duplicated(keep='first')]
    # remove duplicate rows, keeping only the first instance
    df = df[~df.index.duplicated(keep='first')]
    return df

if __name__ == '__main__':
    df = Data_final(attr,gages)
    df.reset_index().to_csv(final_path, index=False)
    print('saved to {}'.format(wrk_dir))
