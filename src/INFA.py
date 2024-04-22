import pandas as pd
import numpy as np
from scipy.stats import zscore

# Assuming data is already read according to your file format and path
speed_df = pd.read_csv("data/speed.txt", delimiter='\t')
population_df = pd.read_csv("data/population_pct_analysis.txt", delimiter='\t')

# Convert data type of 'tract' and 'geo_id' columns to string for merging
speed_df['id'] = speed_df['tract'].astype(str)
population_df['geo_id'] = population_df['geo_id'].astype(str)

# Merge datasets
merged_df = pd.merge(speed_df, population_df, left_on='id', right_on='geo_id', how='inner')

# Ensure relevant columns are numeric
merged_df['pct_no_internet'] = pd.to_numeric(merged_df['pct_no_internet'])
merged_df['pct_no_computer'] = pd.to_numeric(merged_df['pct_no_computer'])
merged_df['mean_max_advertised_download_speed'] = pd.to_numeric(merged_df['mean_max_advertised_download_speed'])
merged_df['mean_max_advertised_upload_speed'] = pd.to_numeric(merged_df['mean_max_advertised_upload_speed'])

# Calculate Z-scores
merged_df['DNS_z'] = zscore(merged_df['mean_max_advertised_download_speed'])
merged_df['UPS_z'] = zscore(merged_df['mean_max_advertised_upload_speed'])

# Calculate NIA and NCD values
merged_df['NIA'] = merged_df['pct_no_internet']
merged_df['NCD'] = merged_df['pct_no_computer']

# Calculate INFA score using Z-scores
merged_df['INFA'] = merged_df['NIA'] * 0.35 + merged_df['NCD'] * 0.35 - merged_df['DNS_z'] * 0.15 - merged_df['UPS_z'] * 0.15

# Scale INFA score to range 0 to 100
merged_df['INFA_scaled'] = 100 * (merged_df['INFA'] - merged_df['INFA'].min()) / (merged_df['INFA'].max() - merged_df['INFA'].min())


# Output results
infa_scaled = merged_df[['id', 'INFA_scaled']]
print(infa_scaled)

# Save to CSV file
#merged_df[['id', 'INFA_scaled']].to_csv("data/infa_scaled.csv")
