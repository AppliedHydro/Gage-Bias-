import pandas as pd

def uniques(file_path, column_name):
    try:
        df = pd.read_csv(file_path)
        unique_values = df[column_name].unique()

        return unique_values

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

file_path = 'H:/Catalog_Subsets/Streamflow_Catalog.csv'
column_name = 'ecoregion'  

unique_values = uniques(file_path, column_name)

if unique_values is not None:
    print(f"Unique values in {column_name}:")
    for value in unique_values:
        print(value)
