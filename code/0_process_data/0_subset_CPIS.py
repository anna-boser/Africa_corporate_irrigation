# This file reads the CPIS shapefiles and the Africa shapefile, and filters the CPIS shapefiles to only include the countries in Africa.

import yaml
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import utils

# Load the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Read the shapefiles
CPIS2000 = gpd.read_file(config["CPIS_2000_shp_path"])
CPIS2021 = gpd.read_file(config["CPIS_2021_shp_path"])
Africa = gpd.read_file(config["Africa_countries_shp_path"])

# Rename the country name column in the Africa shapefile from "NAME_0" to "Country"
Africa = Africa.rename(columns={'NAME_0': 'Country', 'ISO' : 'Country Code'}) # Unfortunately 'Country Code' will be renamed to 'Country Co' when saving due to a 10-character limit on shapefiles.

# Remove the 'OBJECTID', 'Continent', 'REgion' columns
Africa = Africa.drop(columns=['OBJECTID', 'Continent', 'REgion'])

# Save this shapefile
Africa.to_file(config["Africa_countries_shp_path"])

# Perform the spatial intersection
CPIS2000_Africa = gpd.overlay(CPIS2000, Africa, how='intersection')
CPIS2021_Africa = gpd.overlay(CPIS2021, Africa, how='intersection')

# Save the intersected shapefile
CPIS2000_Africa.to_file(config["Africa_CPIS_2000_shp_path"])
CPIS2021_Africa.to_file(config["Africa_CPIS_2021_shp_path"])

# # Read the shapefiles
# CPIS2000_Africa = gpd.read_file(config["Africa_CPIS_2000_shp_path"])
# CPIS2021_Africa = gpd.read_file(config["Africa_CPIS_2021_shp_path"])
# Africa = gpd.read_file(config["Africa_countries_shp_path"])

# Add a 'year' column to each dataframe
CPIS2000_Africa['Year'] = 2000
CPIS2021_Africa['Year'] = 2021

# Merge the two dataframes
CPIS_Africa = gpd.GeoDataFrame(pd.concat([CPIS2000_Africa, CPIS2021_Africa], ignore_index=True))

# Save the merged shapefile
CPIS_Africa.to_file(config["Africa_CPIS_shp_path"])

# Buffer the geometry to make it more visible
CPIS_Africa['geometry'] = CPIS_Africa.geometry.buffer(0.1)

# Create a single plot with two facets
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Plot the CPIS data for 2000
Africa.boundary.plot(ax=axes[0], color='black')
CPIS_Africa[CPIS_Africa['Year'] == 2000].plot(ax=axes[0], color='green')
axes[0].set_title('CPIS in 2000 in Africa')

# Plot the CPIS data for 2021
Africa.boundary.plot(ax=axes[1], color='black')
CPIS_Africa[CPIS_Africa['Year'] == 2021].plot(ax=axes[1], color='green')
axes[1].set_title('CPIS in 2021 in Africa')

# Adjust layout and show the plot
plt.tight_layout()
plt.show()

# Save the combined figure
fig.savefig(utils.make_output_path('CPIS_2000_2021_Africa.png'))
