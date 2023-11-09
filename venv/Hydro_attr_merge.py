#Hydro_attr_marge.py
#
#This script clips the primary HydroATLAS attributes file to the Pacific Northwest - the scope of our gage dataset. It also deletes
#older streamflow gage information merged into the attribute data and prepares it to be updated with new gage data.
#columns removed: stationid, lat, long, distance

import pandas as pd

wrk_dir = 'H:/'
hydro_attr = wrk_dir + 'HydroATLAS/Krabbenhoft_etal_2022_NatSus_Stream_characteristics_data/Attribute_table_final.csv'
hydro_river = wrk_dir + 'HydroATLAS/HydroATLAS_PNW.csv'#HydroATLAS river segments clipped to PNW

# check to confirm that REACH_ID is in the loaded data - this will be used as index for merge with HydroATLAS river segments
try:
    df1 = pd.read_csv(hydro_attr)
    if 'REACH_ID' not in df1.columns:
        print(f"Error: REACH_ID column not found in {hydro_attr}")
        exit()
except FileNotFoundError:
    print(f"Error: {hydro_attr[-25:]} not found.")
    exit()

try:
    df2 = pd.read_csv(hydro_river)
    if 'REACH_ID' not in df2.columns:
        print(f"Error: REACH_ID column not found in {hydro_river}")
        exit()
except FileNotFoundError:
    print(f"Error: {} not found.") #add hydro filename index
    exit()

# merge the two DataFrames using REACH_ID as the index
merged_df = pd.merge(df1, df2, on='REACH_ID', how='inner')

# check if there are any null values in the REACH_ID column
if merged_df['REACH_ID'].isnull().any():
    print("Error: Merge failed. Check the REACH_ID column for missing values.")
    exit()

# check the length of the merged DataFrame
if len(merged_df) == len(df2):
    print("Lengths match!")
else:
    print("Lengths do not match. Potential error with merge.")
    exit()

# check for duplicates in the merged dataframe
if merged_df.duplicated(subset='REACH_ID').any():
    print("Duplicates found in the merged DataFrame. Please check your data.")
    exit()

columns_remove = ['Unnamed: 0','stationid','lat','long','distance','noFlowGauge','continent']
df_final = merged_df.drop(columns=columns_remove)

df_final.to_csv(wrk_dir + 'HydroATLAS/HydroATLAS_final.csv', index=False)