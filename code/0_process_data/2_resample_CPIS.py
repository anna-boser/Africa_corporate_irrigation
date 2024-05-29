# This script counts the number of CPIS in the year 2000 and 2021 for each country in Africa.
# It then produces a map of the % change in CPIS between 2000 and 2021.

import yaml
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import utils

# Load the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Read the shapefiles
CPIS2000_Africa = gpd.read_file(config["Africa_CPIS_2000_shp_path"])
CPIS2021_Africa = gpd.read_file(config["Africa_CPIS_2021_shp_path"])

# Count the number of CPIS in each year for each country
country_counts_2000 = CPIS2000_Africa['NAME_0'].value_counts()
country_counts_2000 = country_counts_2000.reset_index() # Convert the Series to a DataFrame
country_counts_2000.columns = ['NAME_0', 'CPIS_2000'] # Rename the columns

# Repeat the process for 2021
country_counts_2021 = CPIS2021_Africa['NAME_0'].value_counts()
country_counts_2021 = country_counts_2021.reset_index() # Convert the Series to a DataFrame
country_counts_2021.columns = ['NAME_0', 'CPIS_2021'] # Rename the columns

# Combine the counts into a single dataframe by merging on the country name
country_counts = country_counts_2000.merge(country_counts_2021, on='NAME_0')

# Calculate the change in CPIS between 2000 and 2021
country_counts['change'] = ((country_counts['CPIS_2021'] - country_counts['CPIS_2000'])) * 100

# save the country_counts dataframe
country_counts.to_csv(config['country_CPIS_count'], index=False)

# Merge the change with the Africa shapefile
Africa = gpd.read_file(config["Africa_countries_shp_path"])
Africa_counts = Africa.merge(country_counts, on='NAME_0')

# Plot the change in CPIS between 2000 and 2021
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
Africa.boundary.plot(ax=ax, color = 'black')
Africa_counts.plot(column='change', cmap='Blues', legend=True, ax=ax)
ax.set_title('Change in CPIS between 2000 and 2021')
plt.show()

# Save the figure
fig.savefig(utils.make_output_path("CPIS_change_country_map.png"))

# Map the number of CPIS in 2000
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
Africa.boundary.plot(ax=ax, color = 'black')
Africa_counts.plot(column='CPIS_2000', cmap='Blues', legend=True, ax=ax)
ax.set_title('Number of CPIS in 2000')
plt.show()

# Save the figure
fig.savefig(utils.make_output_path("CPIS_2000_country_map.png"))

# Map the number of CPIS in 2021
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
Africa.boundary.plot(ax=ax, color = 'black')
Africa_counts.plot(column='CPIS_2021', cmap='Blues', legend=True, ax=ax)
ax.set_title('Number of CPIS in 2021')
plt.show()

# Save the figure
fig.savefig(utils.make_output_path("CPIS_2021_country_map.png"))

#plot both 2000 and 2021 CPIS on the same map
# Create a normalization instance with the min and max values across both columns
vmin = min(Africa_counts['CPIS_2000'].min(), Africa_counts['CPIS_2021'].min())
vmax = max(Africa_counts['CPIS_2000'].max(), Africa_counts['CPIS_2021'].max())
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Plot the number of CPIS in 2000
Africa.boundary.plot(ax=axes[0], color='black')
Africa_counts.plot(column='CPIS_2000', cmap='Blues', norm=norm, legend=True, ax=axes[0])
axes[0].set_title('Number of CPIS in 2000')

# Plot the number of CPIS in 2021
Africa.boundary.plot(ax=axes[1], color='black')
Africa_counts.plot(column='CPIS_2021', cmap='Blues', norm=norm, legend=True, ax=axes[1])
axes[1].set_title('Number of CPIS in 2021')

# Adjust layout
plt.tight_layout()

# Show the combined plot
plt.show()

# Save the figure
fig.savefig('CPIS_2000_2021_country_map.png')