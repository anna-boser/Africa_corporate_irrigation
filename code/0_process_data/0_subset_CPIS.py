# This file reads the CPIS shapefiles and the Africa shapefile, and filters the CPIS shapefiles to only include the countries in Africa.

import yaml
import geopandas as gpd

# Load the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Read the shapefiles
CPIS2000 = gpd.read_file(config["CPIS_2000_shp_path"])
CPIS2021 = gpd.read_file(config["CPIS_2021_shp_path"])
Africa = gpd.read_file(config["Africa_countries_shp_path"])

# Perform the spatial intersection
CPIS2000_Africa = gpd.overlay(CPIS2000, Africa, how='intersection')
CPIS2021_Africa = gpd.overlay(CPIS2021, Africa, how='intersection')

# Save the intersected shapefile
CPIS2000_Africa.to_file(config["Africa_CPIS_2000_shp_path"])
CPIS2021_Africa.to_file(config["Africa_CPIS_2021_shp_path"])
