import pandas as pd

# file paths for HydroATLAS attributes file and GRADES/gage .csv
wrk_dir = 'H:/'
attr = wrk_dir + 'HydroATLAS/HydroATLAS_final.csv'
gages = wrk_dir + 'GRADES/GRADES_gage_discrete.csv'

def Data_final(attr,gages):
    df_A, df_B = pd.read_csv(attr),pd.read_csv(gages)
    assert not df_A.empty,"{} is empty. Reload.".format(attr)
    assert not df_B.empty,"{} is empty. Reload.".format(gages)

    # merge the DataFrames based on COMID
    merged_df = pd.merge(df_A, df_B[['COMID', 'Gage_No', 'lat', 'long']], on='COMID', how='left')
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
    df.reset_index().to_csv('H:/Final_data_discrete.csv', index=False)
    print('saved to {}'.format(wrk_dir))