# Take the combined data and pivot it longer so you have one column for the year and one column for whether it was detected in that year.

import pandas as pd
import geopandas as gpd
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

combined_gdf = gpd.read_file(config["combined_CPIS_shp_path"])

# Pivot longer using pd.melt
long_gdf = pd.melt(combined_gdf,
                   id_vars=['ID', 'Country', 'Country Co', 'geometry'],
                   value_vars=['year_2000', 'year_2021'],
                   var_name='Year',
                   value_name='Detected')

# Replace 'year_2000' and 'year_2021' with '2000' and '2021' respectively
long_gdf['Year'] = long_gdf['Year'].replace({'year_2000': 2000, 'year_2021': 2021})

# Convert back to a GeoDataFrame
long_gdf = gpd.GeoDataFrame(long_gdf, geometry='geometry')

# save the panel
long_gdf.to_file(config["empty_panel_CPIS_shp_path"])