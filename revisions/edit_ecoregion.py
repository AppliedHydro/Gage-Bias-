# This script is used for converting string ecoregion values into integers to be useable in placement analysis script

import pandas as pd

data = 'H:/Final_data.csv'
output_path = 'XXXX.csv'

# Read the CSV file into a pandas 
df = pd.read_csv(data)

# dict for ascribing integer values to ecoregion string
eco_val = {'nan' : 1, 'Blue Mountains' : 1, 'Northern Basin and Range' : 2, 'Eastern Cascades Slopes and Foothills' : 3,
           'Cascades' : 4, 'Klamath Mountains/California High North Coast Range' : 5, 'Northern Rockies' : 6,
           'Strait of Georgia/Puget Lowland' : 7, 'North Cascades' : 8, 'Columbia Plateau' : 9,
           'Coast Range' : 10, 'Idaho Batholith' : 11, 'Willamette Valley' : 12, 'Middle Rockies' : 13,
           'Snake River Plain' : 14}

eco_col = 'ecoregion'
df[eco_col] = df[eco_col].replace(eco_val)
# convert floats to integers, ignoring NaN values
df[eco_col] = pd.to_numeric(df[eco_col], errors='coerce').astype('Int64')
df.to_csv(output_path, index=False)
