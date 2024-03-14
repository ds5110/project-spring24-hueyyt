import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_population_map(population_df_path, tracts_geojson_path):
    """
    Plot a map showing the over 60 population per census tract.

    :param population_df_path: Path to the Excel file containing population data.
    :param tracts_geojson_path: Path to the GeoJSON file containing census tract boundaries.
    """
    # Read population data from Excel file
    population_df = pd.read_excel(population_df_path, sheet_name=1)

    # Filter rows where 'geo_id' starts with '230'
    population_df = population_df[population_df['geo_id'].astype(str).str.startswith('230')]

    # Read census tract boundaries
    tracts_gdf = gpd.read_file(tracts_geojson_path)

    # Merge population data with census tract boundaries
    merged_gdf = tracts_gdf.merge(population_df, left_on='GEOID', right_on='geo_id', how='left')

    # Plotting
    plt.figure(figsize=(10, 8))
    ax = merged_gdf.plot(column='pct_no_bb_or_computer_pop', cmap='YlOrRd', linewidth=0.5, edgecolor='grey', legend=True)
    plt.title('Percentage of Population without Broadband or Computer by Census Tract')
    plt.axis('off')
    plt.show()

# Paths to data files
population_df_path = "data/county_tract_total_covered_populations.xlsx"
tracts_geojson_path = "docs/INFA_scaled.json"

# Generate and display the map
plot_population_map(population_df_path, tracts_geojson_path)
