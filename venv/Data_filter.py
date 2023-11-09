import pandas as pd
'''
# Define file paths
global_attr = 'H:/Attriutes.csv'
local_attr = 'H:/GRADES/GRADES_Hydro_Join.csv'

# Read both CSV files
print('importing files...')
df_glob = pd.read_csv(global_attr)
df_loc = pd.read_csv(local_attr)

# Get the set of unique COMID values from file B
print('filtering...')
comids_loc = set(df_loc['COMID'])

# Filter rows in file A to keep only those with COMID values present in file B
df_glob_filtered = df_glob[df_glob['COMID'].isin(comids_loc)]
print('saving...')

# Save the filtered DataFrame back to a new CSV file
df_glob_filtered.to_csv('H:/filtered_attributes.csv', index=False)
print('file saved to H:/')

# Define file paths
attr = 'H:/filtered_attributes.csv'
gages = 'H:/GRADES/GRADES_gage.csv'

# Read both CSV files
df_A = pd.read_csv(attr)
df_B = pd.read_csv(gages)

# Merge the DataFrames based on COMID
merged_df = pd.merge(df_A, df_B[['COMID', 'Gage_No', 'lat', 'long']], on='COMID', how='left')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('H:/Final_data.csv', index=False)
'''
file_path = 'H:/Final_data.csv'

# Read the CSV file and set 'COMID' as the index
df = pd.read_csv(file_path)
df.set_index('COMID', inplace=True)

# Check for duplicate rows based on 'COMID' index
duplicate_rows = df[df.index.duplicated(keep='first')]

# Remove duplicate rows, keeping only the first instance
df = df[~df.index.duplicated(keep='first')]

# Save the modified DataFrame back to the CSV file
df.reset_index().to_csv('H:/Final_data_nodupl.csv', index=False)