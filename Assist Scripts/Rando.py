import pandas as pd

def clean_ecoregion_column(csv_file, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Process the 'ecoregion' column and keep only the first two values
    df['ecoregion'] = df['ecoregion'].str.extract(r'^(\d+)')
    
    # Save the DataFrame with the cleaned 'ecoregion' column to a new CSV file
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    # Specify the input CSV file and the output CSV file
    input_csv_file = "H:/Final_data.csv"
    output_csv_file = "H:/Final_data.csv"

    # Call the function to clean the 'ecoregion' column and save the result
    clean_ecoregion_column(input_csv_file, output_csv_file)
