import pandas as pd

def add_gage_numbers(csv_file, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Add a new column 'Gage_No' with values from 1 to the end of the DataFrame
    df['Gage_No'] = range(1, len(df) + 1)

    # Save the DataFrame with the new column to a new CSV file
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    # Specify the input CSV file and the output CSV file
    input_csv_file = "H:/Catalog_Subsets/Streamflow_Catalog.csv"
    output_csv_file = "H:/Catalog_Subsets/Streamflow_Catalog.csv"

    # Call the function to add 'Gage_No' column and save the result
    add_gage_numbers(input_csv_file, output_csv_file)
