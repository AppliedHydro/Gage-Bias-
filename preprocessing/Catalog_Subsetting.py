#----------#
# Takes streamflow catalog and filters out gages based on association in case user
# wants to test for bias for specific organizations
#----------#

import pandas as pd

wrk_dir = 'H:/Catalog_Subsets/'
cat_dir = 'C:/Users/stevenschmitz/Desktop/PlacementBias/Streamflow_Catalog.csv'

err_msg = 'Dataframe not loaded correctly - check output'
df = pd.read_csv(cat_dir)

# Defining functions of code subsetting
def get_USGS(df) -> pd.DataFrame:
    """
    Takes the Streamflow Catalog and filters out all rows that are not
    affiliated with USGS by checking the organization name and the
    organization dataset.
    :param df: streamflow catalog as pd.DataFrame object
    :return: df_usgs; pd.DataFrame of USGS gages
    """
    df_usgs = df[(df['organization dataset'] == 'USGS') | (df['organization'] == 'United States Geological Survey')]
    df_usgs  = df_usgs.assign(Gage_No=range(1, len(df_usgs) + 1))
    assert not df_usgs.empty, err_msg
    print('df_usgs has {} gages'.format(len(df_usgs)))
    df_usgs.to_csv(wrk_dir + 'USGS_cat.csv',index=False)
    return df_usgs

def get_cont(df) -> pd.DataFrame:
    """
    Takes Streamflow Catalog and filters out all rows that are designated
    as continuous gages (meas.freq == 'continuous').
    :param df: streamflow catalog as pd.DataFrame object
    :return: df_cont; pd.DataFrame of continuous gages
    """
    df_cont = df[df['meas.freq'] == 'continuous']
    df_cont = df_cont.assign(Gage_No=range(1, len(df_cont) + 1))
    assert not df_cont.empty, err_msg
    print('df_cont has {} gages'.format(len(df_cont)))
    df_cont.to_csv(wrk_dir + 'Cont_cat.csv',index=False)
    return df_cont

def get_disc(df) -> pd.DataFrame:
    """
    Takes Streamflow Catalog and filters out all rows that are designated
    as discrete gage measurements (meas.freq == 'discrete').
    :param df: streamflow catalog as pd.DataFrame object
    :return: df_disc; pd.DataFrame of discrete gages
    """
    df_disc = df[df['meas.freq'] == 'discrete']
    df_disc = df_disc.assign(Gage_No=range(1, len(df_disc) + 1))
    assert not df_disc.empty, err_msg
    print('df_disc has {} gages'.format(len(df_disc)))
    df_disc.to_csv(wrk_dir + 'Discrete_cat.csv',index=False)
    return df_disc

# Initialization point of the code

# Excel spreadsheet with callable columns
column_file = #####
print('Refer to {} for a list of columns names. Use column names as input to '
      'uniques() in string format to find all available unique values in'
      'that column. These unique values can be used as inputs to create new'
      '.xlsx with subset gages.'.format(column_file))

def uniques(file_path, sheet_name = 'Sheet1', column_name):
    '''
    Reads unique columns values to be used for subsetting the output streamflow catalog.
    :param file_path: file path of streamflow catalog
    :param sheet_name: in default streamflow catalog, Sheet1 is the primary catalog sheet.
    :param column_name: column to find unique values from.
    :return: list of unique values
    '''
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        unique_values = df[column_name].unique()
        return unique_values
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def master_subset(file_path, column_name, target_value,output_path):
    try:
        df = pd.read_excel(file_path)
        filtered_df = df[df[column_name] == target_value]
        filtered_df.to_csv(output_path, index=False)
        print(f"Rows with '{target_value}' saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    #Filter catalog for USGS gages
    get_USGS(df)
    print('USGS catalog saved to ' + wrk_dir + '...')

    #Filter catalog for continuous gages
    get_cont(df)
    print('Continuous catalog saved to ' + wrk_dir + '...')

    #Filter catalog for discrete gages
    get_disc(df)
    print('Discrete catalog saved to ' + wrk_dir + '...')
