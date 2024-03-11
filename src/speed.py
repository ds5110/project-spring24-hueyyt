import pandas as pd
import numpy as np

def read_fcc(filename, columnname):
    """
    Read 'bdc_23_....zip' files and calculate the median download or upload speed.
    """
    df = pd.read_csv(filename, dtype={'block_geoid': str})
    df = df.rename(columns={"block_geoid": "block_fips"})
    # Extract the tract-level identifier (the first 11 digits of block_fips)
    df['tract'] = df['block_fips'].str[:11]
    return df.groupby("tract")[columnname].median()

def get_clean_max(download_df, upload_df):
    """
    Clean and merge download and upload speed data, calculating the average speed.
    """
    download_df = download_df.rename(columns={"max": "mean_max_advertised_download_speed"})
    upload_df = upload_df.rename(columns={"max": "mean_max_advertised_upload_speed"})
    combined_df = download_df.merge(upload_df, how='left', left_index=True, right_index=True)
    return combined_df.reset_index()

def calculate_average_speeds(filenames):
    """
    For a given list of filenames, calculate the average download and upload speeds.
    """
    block_download_speeds = {filename.split("_")[2]: read_fcc(filename, "max_advertised_download_speed")
                             for filename in filenames}
    block_upload_speeds = {filename.split("_")[2]: read_fcc(filename, "max_advertised_upload_speed")
                           for filename in filenames}

    df_download = pd.DataFrame(block_download_speeds).max(axis=1).to_frame(name='max')
    df_upload = pd.DataFrame(block_upload_speeds).max(axis=1).to_frame(name='max')
    
    return get_clean_max(df_download, df_upload)

filenames = [
    "data/bdc_23_Cable_fixed_broadband_J23_05mar2024.zip",
    "data/bdc_23_Copper_fixed_broadband_J23_05mar2024.zip",
    "data/bdc_23_FibertothePremises_fixed_broadband_J23_05mar2024.zip",
    "data/bdc_23_LicensedFixedWireless_fixed_broadband_J23_05mar2024.zip"
]

average_speeds_df = calculate_average_speeds(filenames)
print(average_speeds_df)


average_speeds_df.to_csv('data/speed.txt', index=False, sep='\t')


