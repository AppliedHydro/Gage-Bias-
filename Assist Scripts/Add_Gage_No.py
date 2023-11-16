import pandas as pd

def add_gage_numbers(csv_file, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    df['Gage_No'] = range(1, len(df) + 1)
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    # input and output files
    input_csv_file = "H:/Catalog_Subsets/Streamflow_Catalog.csv"
    output_csv_file = "H:/Catalog_Subsets/Streamflow_Catalog.csv"
    add_gage_numbers(input_csv_file, output_csv_file)
