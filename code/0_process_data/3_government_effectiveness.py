# Add the government effectiveness index to the CPIS data

import geopandas as gpd
import pandas as pd
import utils
import yaml

# Load the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# read in the government effectiveness index data
GEI = pd.read_csv(config["government_effectiveness_path"]) 

# Rename the GEI "Country Name" column to "NAME_0" to match the CPIS data
GEI = GEI.rename(columns={'Country Name': 'Country', 'Country Code' : 'Country Co'}) # unfortunately 'Country Co' was renamed to 'Country Co_' in other files when saving due to a 10-character limit on shapefiles.

# pivot the GEI data so the year becomes one column
GEI = pd.melt(GEI, id_vars=['Country', 'Country Co'], var_name='Year', value_name='GEI')

# Convert the year column to integer
GEI['Year'] = GEI['Year'].astype(int)

# Add a two year and four year lag GEI variable to the GEI data
GEI = utils.create_lagged_column(GEI, 'GEI', 2)
GEI = utils.create_lagged_column(GEI, 'GEI', 4)

# read in the 2000 and 2021 cpis data
CPIS = gpd.read_file(config["empty_panel_CPIS_shp_path"])

# Add GEI information to the CPIS data by matching on year and country
CPIS = CPIS.merge(GEI, on=['Year', 'Country', 'Country Co'])

# Save the CPIS data with GEI information
CPIS.to_file(config["CPIS_GEI_shp_path"])