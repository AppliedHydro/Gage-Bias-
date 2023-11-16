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
