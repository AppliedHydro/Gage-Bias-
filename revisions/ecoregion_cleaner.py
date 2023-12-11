# As of 11.16, this script is necessary to clean the ecoregion variables and reduce them to integers only - removing string values. The placement analysis code cannot handle string values for
# ecoregion variables - integers only.
# date: 11.16.2023

import pandas as pd

def clean_ecoregion_column(csv_file, output_csv):
    df = pd.read_csv(csv_file) # catalog with ecoregion column
    df['ecoregion'] = df['ecoregion'].str.extract(r'^(\d+)') # keep integer values of ecoregions
    
    # Save the DataFrame with the ecoregion column to CSV file
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    input_csv_file = "H:/Final_data.csv"
    output_csv_file = "H:/Final_data.csv"
    clean_ecoregion_column(input_csv_file, output_csv_file)
