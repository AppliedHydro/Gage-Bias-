import warnings
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

err_msg = 'Dataframe not loaded correctly - check output'

def setup():
    print("Library setup complete.")
