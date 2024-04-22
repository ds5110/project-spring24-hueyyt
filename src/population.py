import pandas as pd

def print_geoid_and_pct_from_csv(filename):
    """
    Read a CSV file and calculate the percentage of population without internet access (NIA)
    and without computing devices (NCD) for rows where 'GEO_ID' starts with '1400000US230'.
    Save the same data to a txt file.
    
    :param filename: The path to the CSV file.
    """
    # Read the CSV file
    population_df = pd.read_csv(filename)
    
    # Filter rows where 'GEO_ID' starts with '1400000US230'
    filtered_df = population_df[population_df['GEO_ID'].astype(str).str.startswith('1400000US230')].copy()
    
    # Correctly modify a column in place using .loc
    filtered_df.loc[:, 'GEO_ID'] = filtered_df['GEO_ID'].str.replace('1400000US', '')
    
    # Replace non-convertible values with NaN before converting to float
    filtered_df['S2802_C07_001E'] = pd.to_numeric(filtered_df['S2802_C07_001E'], errors='coerce')
    filtered_df['S2802_C05_001E'] = pd.to_numeric(filtered_df['S2802_C05_001E'], errors='coerce')
    
    # Calculate NIA and NCD
    filtered_df['NIA'] = filtered_df['S2802_C07_001E'] + filtered_df['S2802_C05_001E']
    filtered_df['NCD'] = filtered_df['S2802_C07_001E']
    
    # Select only relevant columns
    relevant_df = filtered_df[['GEO_ID', 'NIA', 'NCD']]
    
    # Rename columns for clarity
    relevant_df.columns = ['geo_id', 'pct_no_internet', 'pct_no_computer']
    
    # Print 'geo_id', 'pct_no_internet', and 'pct_no_computer'
    print(relevant_df)
    
    # Save 'geo_id', 'pct_no_internet', and 'pct_no_computer' to a txt file
    relevant_df.to_csv('data/population_pct_analysis.txt', index=False, sep='\t')

# The path to the CSV file
file_path = 'data/ACSST5Y2022.S2802-Data.csv'

# Call the function
print_geoid_and_pct_from_csv(file_path)
