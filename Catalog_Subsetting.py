import pandas as pd

wrk_dir = 'H:/Catalog_Subsets/'
cat_dir = 'C:/Users/stevenschmitz/Desktop/PlacementBias/Streamflow_Catalog.csv'

err_msg = 'Dataframe not loaded correctly - check output'
df = pd.read_csv(cat_dir)

def get_USGS(df) -> pd.DataFrame:
    """
    Takes the Streamflow Catalog and filters out all rows that are not
    affiliated with USGS by checking the organization name and the
    organization dataset.
    :param df: streamflow catalog as pd.DataFrame object
    :return: df_usgs; pd.DataFrame of USGS gages
    """
    df_usgs = df[(df['organization dataset'] == 'USGS') | (df['organization'] == 'United States Geological Survey')]
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
    assert not df_disc.empty, err_msg
    print('df_disc has {} gages'.format(len(df_disc)))
    df_disc.to_csv(wrk_dir + 'Discrete_cat.csv',index=False)
    return df_disc

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