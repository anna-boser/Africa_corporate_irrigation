# regression testing the effect of government effectiveness on CP expansion

import geopandas as gpd
import pandas as pd
import yaml

# Load the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

CPIS = gpd.read_file(config["CPIS_GEI_shp_path"])

# first, panel regression looking at the effect of GEI on "Detected" column