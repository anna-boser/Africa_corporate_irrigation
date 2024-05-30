# Add SPEI drought index to the CPIS data

import geopandas as gpd
import pandas as pd
import utils
import yaml

# Load the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# read in the government effectiveness index data
SPEI = pd.read_csv(config["SPEI_12_path"]) 

# Rename the SPEI "Country Name" column to "NAME_0" to match the CPIS data
SPEI = SPEI.rename(columns={'Country Name': 'Country', 'Country Code' : 'Country Co'}) # unfortunately 'Country Co' was renamed to 'Country Co_' in other files when saving due to a 10-character limit on shapefiles.

# pivot the SPEI data so the year becomes one column
SPEI = pd.melt(SPEI, id_vars=['Country', 'Country Co'], var_name='Year', value_name='SPEI')

# Convert the year column to integer
SPEI['Year'] = SPEI['Year'].astype(int)

# Add a two year and four year lag SPEI variable to the SPEI data
SPEI = utils.create_lagged_column(SPEI, 'SPEI', 5)

# read in the 2000 and 2021 cpis data
CPIS = gpd.read_file(config["CPIS_GEI_shp_path"])

# Add SPEI information to the CPIS data by matching on year and country
CPIS = CPIS.merge(SPEI, on=['Year', 'Country', 'Country Co'])

# Save the CPIS data with SPEI information
CPIS.to_file(config["CPIS_SPEI_shp_path"])