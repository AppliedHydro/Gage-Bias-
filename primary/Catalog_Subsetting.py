# Catalog_Subsetting.py
#
# Author: Steven Schmitz
# date: 11.16.2023
#
# This code functions as a filtering script to produce new versions of the Streamflow Catalog
# <https://github.com/AppliedHydro/StreamflowCatalog> sorted by variables of interest to be used in the
# Placement Analysis <https://github.com/AppliedHydro/Gauge-Placement-Analysis> project. The file output from this
# script can be input directly into the analysis script per ReadMe instructions.

import warnings
import pandas as pd

wrk_dir = 'H:/Catalog_Subsets/'                # working directory
cat_dir = wrk_dir + 'Streamflow_Catalog.csv'   # Streamflow catalog csv file
column_file = 'H:/subset_options.xlsx'         # Excel spreadsheet with callable columns
file_final = 'XXXX.csv'                        # Output file name

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

def master_subset(catalog_path, column_name, target_value, output_path):
    '''
    Master subsetting function, saves filtered catalog to output file path to be used
    for placement analysis.
    :param catalog_path: directory of streamflow catalog in .csv format
    :param column_name: name of catalog column that target_value is coming from
    :param target_value: value used for filtering the catalog
    :param output_path: save location for filtered catalog as csv
    :return: pd.DataFrame of filtered catalog
    '''
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=pd.errors.DtypeWarning)
            df = pd.read_csv(catalog_path)
            if column_name == 'huc4':
                target_value = int(target_value)
            filtered_df = df[df[column_name] == target_value]
            assert not filtered_df.empty, "No matching rows found."
            filtered_df.to_csv(output_path, index=False)
            print(f"Rows with '{target_value}' saved to {output_path}")
            return filtered_df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    print('Refer to {} for column_name and target_value options to filter the'
          ' gages. File output will be the Streamflow catalog subset to'
          'including only gages that match the target value.'.format(column_file))
    master_subset(cat_dir, 'status', 'active', wrk_dir + file_final)

