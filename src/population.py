import pandas as pd

def print_geoid_and_pct(filename):
    """
    Read an Excel file and print 'geo_id' and 'pct_no_bb_or_computer_pop' columns for rows where 'geo_id' starts with '230'.
    Save the same data to a txt file.
    
    :param filename: The path to the county_tract_total_covered_populations.xlsx file.
    """
    # Read the Excel file
    population_df = pd.read_excel(filename, sheet_name=1)

    # Filter rows where 'geo_id' starts with '230'
    filtered_df = population_df[population_df['geo_id'].astype(str).str.startswith('230')]

    # Print 'geo_id' and 'pct_no_bb_or_computer_pop'
    print(filtered_df[['geo_id', 'pct_no_bb_or_computer_pop']])

    # Save 'geo_id' and 'pct_no_bb_or_computer_pop' to a txt file
    filtered_df[['geo_id', 'pct_no_bb_or_computer_pop']].to_csv('data/population.txt', index=False, sep='\t')


excel_file_path = "data/county_tract_total_covered_populations.xlsx" 

print_geoid_and_pct(excel_file_path)
