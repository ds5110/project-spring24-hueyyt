# SE data collection and calculation - result saved to SE_score.csv

# libraries
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import requests

# helpful function - reset the dataframe index
def set_index(df):
    df.columns = df.iloc[0]
    df.drop(index=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

# helpful function - standardize the score
def standardize_score(df, i):
  mean = df[i].mean()
  std = df[i].std()
  result = (df[i] - mean) / std
  return result

# variables
geog = '&for=tract:*&in=state:23&in=county:*'
geog_rural = '&for=block:*&in=state:23+county:*+tract:*'

subject_table = 'https://api.census.gov/data/2022/acs/acs5/subject?get='
detailed_table = 'https://api.census.gov/data/2022/acs/acs5?get='
profile_table = 'https://api.census.gov/data/2022/acs/acs5/profile?get='
cprofile_table = 'https://api.census.gov/data/2022/acs/acs5/cprofile?get='
responserate_table = 'https://api.census.gov/data/2020/dec/dhc?get=group(P2)'

# B01001_001E: Total population of Maine
# B26103_004E: Incarcerated individuals
# B21001_002E: Veterans

key_detailed = ['B01001_001E','B26103_004E','B21001_002E']
url_detailed = detailed_table + ",".join(key_detailed) + geog
df_detailed = pd.read_json(url_detailed)

df_detailed.columns = df_detailed.iloc[0]
df_detailed = df_detailed[1:]

df_detailed.rename(columns={'B01001_001E': 'totalpop'}, inplace=True)
df_detailed['totalpop'] = pd.to_numeric(df_detailed['totalpop'])

df_detailed['vet'] = pd.to_numeric(df_detailed['B21001_002E'], errors='coerce')
df_detailed['per_vet'] = np.where(df_detailed['totalpop'] > 0, df_detailed['vet'] / df_detailed['totalpop'], 0)
df_detailed['z_per_vet'] = standardize_score(df_detailed, 'per_vet')


def fetch_incar():
    url = 'https://api.census.gov/data/2022/acs/acs5?get=B26103_004E&for=state:23'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        total_incarcerated_in_maine = int(data[1][0])
        return total_incarcerated_in_maine
    else:
        print("Error fetching data from Census API")
        return None

incar = fetch_incar()

df_detailed['incar'] = pd.to_numeric(df_detailed['B26103_004E'], errors='coerce')
num_tracts = df_detailed['tract'].nunique()
avg_incar_per_tract = incar / num_tracts
df_detailed['avg_incar_per_tract'] = avg_incar_per_tract
df_detailed['incar'] = df_detailed['avg_incar_per_tract']
df_detailed['per_incar'] = np.where(df_detailed['totalpop'] > 0, df_detailed['incar'] / df_detailed['totalpop'], 0)
df_detailed['z_per_incar'] = standardize_score(df_detailed, 'per_incar')

# S0101_C01_028E: 60 years and over
# S1810_C02_001E: Disabled population

key_subject = ['S0101_C01_028E','S1810_C02_001E']
url_subject = subject_table + ",".join(key_subject) + geog
df_subject = pd.read_json(url_subject)

df_subject.columns = df_subject.iloc[0]  # Set the first row as column names
df_subject = df_subject[1:]  # Remove the first row (redundant column names)

# Calculate proportion of over 60 population and disabled population
df_subject['over60'] = pd.to_numeric(df_subject['S0101_C01_028E'], errors='coerce')
df_subject['per_over60'] = np.where(df_detailed['totalpop'] > 0, df_subject['over60'] / df_detailed['totalpop'], 0)
df_subject['z_per_over60'] = standardize_score(df_subject, 'per_over60')

df_subject['dis'] = pd.to_numeric(df_subject['S1810_C02_001E'], errors='coerce') 
df_subject['per_dis'] = np.where(df_detailed['totalpop'] > 0, df_subject['dis'] / df_detailed['totalpop'], 0)
df_subject['z_per_dis'] = standardize_score(df_subject, 'per_dis')

str_list = ['state', 'county', 'tract']
df_detailed['id'] = df_detailed['state'] + df_detailed['county'] + df_detailed['tract']
df_subject['id'] = df_subject['state'] + df_subject['county'] + df_subject['tract']
df_detailed_res = df_detailed[['id', 'totalpop', 'incar', 'per_incar', 'z_per_incar','vet', 'per_vet', 'z_per_vet']]
df_subject_res = df_subject[['id', 'over60', 'per_over60', 'z_per_over60', 'dis', 'per_dis', 'z_per_dis']]
df_se1 = pd.merge(df_detailed_res, df_subject_res, on='id', how='inner')

#################################################################################################################
# Find the covered populations - Members of a racial or ethnic minority group

minority_code = ['DP05_0072E', 'DP05_0073E', 'DP05_0080E', 'DP05_0081E', 'DP05_0082E',
                 'DP05_0083E', 'DP05_0084E', 'DP05_0085E']
minority_url = profile_table + ','.join(minority_code) + geog
df_minority = pd.read_json(minority_url)
set_index(df_minority)

num_list = ['DP05_0073E', 'DP05_0080E', 'DP05_0081E', 'DP05_0082E', 'DP05_0083E', 'DP05_0084E', 'DP05_0085E']
str_list = ['state', 'county', 'tract']
df_minority[num_list] = df_minority[num_list].apply(pd.to_numeric)
df_minority.rename(columns={'DP05_0072E': 'total_pop'}, inplace=True)
df_minority['minority_pop'] = df_minority.iloc[:, 1:8].sum(axis=1)
df_minority['id'] = df_minority['state'] + df_minority['county'] + df_minority['tract']
df_minority_res = df_minority[['id', 'total_pop', 'minority_pop']]

print('Members of a racial or ethnic minority group')
print(df_minority_res.head())

#################################################################################################################
# Find the covered populations - Rural residents

rural_url = responserate_table + geog_rural
rural_response = requests.get(rural_url)
rural_data = rural_response.json()
df_rural_20 = pd.DataFrame(rural_data)
set_index(df_rural_20)

df_rural_20 = df_rural_20.drop(columns=['P2_001NA', 'P2_002NA', 'P2_003NA', 'P2_004NA'])
df_rural_20.rename(columns={'P2_001N': 'total_pop'}, inplace=True)
df_rural_20.rename(columns={'P2_002N': 'urban_pop'}, inplace=True)
df_rural_20.rename(columns={'P2_003N': 'rural_pop'}, inplace=True)
df_rural_20.rename(columns={'P2_004N': 'not_defined'}, inplace=True)
df_rural_20.rename(columns={'GEO_ID': 'geo_id'}, inplace=True)
df_rural_20[['total_pop', 'urban_pop', 'rural_pop', 'not_defined']] = df_rural_20[['total_pop', 'urban_pop', 'rural_pop', 'not_defined']].apply(pd.to_numeric)
df_rural_20['geo_id'] = df_rural_20['geo_id'].astype(str)
df_rural_20['id'] = df_rural_20['geo_id'].apply(lambda x: x.split("US")[1][:-4])
df_rural_20['id_block'] = df_rural_20['geo_id'].apply(lambda x: x.split("US")[1])

urban_rural_pop_bool = len(df_rural_20[(df_rural_20['urban_pop'] != 0) & (df_rural_20['rural_pop'] != 0)])
not_defined_pop_bool = len(df_rural_20[df_rural_20['not_defined'] != 0])
if urban_rural_pop_bool == 0 and not_defined_pop_bool == 0:
  print('Block level data can be used to assign rural/urban labels.')

# assign rural labels to blocks
df_rural_20['rural'] = np.where((df_rural_20['total_pop'] == df_rural_20['urban_pop']) & (df_rural_20['total_pop'] != 0), 0,
                              np.where((df_rural_20['total_pop'] == df_rural_20['rural_pop']) & (df_rural_20['total_pop'] != 0), 1, None))

# estimate 2022 rural residents based on 2020 data
df_est = df_rural_20.copy()
df_census_tract_20 = df_est.groupby('id')['total_pop'].sum().reset_index()
df_census_tract_20.rename(columns={'total_pop': 'total_pop_20'}, inplace=True)

df_census_tract_22 = df_minority.copy()
df_census_tract_22 = df_census_tract_22[['id', 'total_pop']].copy()
df_census_tract_22.rename(columns={'total_pop': 'total_pop_22'}, inplace=True)

df_census_tract = pd.merge(df_census_tract_20, df_census_tract_22, on='id', how='inner')
df_census_tract['id'] = df_census_tract['id'].astype(str)
df_census_tract['total_pop_22'] = df_census_tract['total_pop_22'].astype(int)

df_est_v2 = df_rural_20.copy()
df_est_v2 = df_est_v2.merge(df_census_tract[['id', 'total_pop_20', 'total_pop_22']], on='id', how='left')
df_est_v2['pop_block_ct'] = df_est_v2['total_pop'] / df_est_v2['total_pop_20']
df_est_v2['est_pop'] = df_est_v2['total_pop_22'] * df_est_v2['pop_block_ct']
est_2022_census_tract_v2 = df_est_v2.groupby('id')['est_pop'].sum().reset_index()
est_2022_census_tract_v2.rename(columns={'est_pop':'est_total_pop_22_v2'}, inplace=True)
df_census_tract = df_census_tract.merge(est_2022_census_tract_v2, on='id', how='left')
rural_2022_block_v2 = df_est_v2[df_est_v2['rural'] == 1]
rural_est_2022_census_tract_v2 = rural_2022_block_v2.groupby('id')['est_pop'].sum().reset_index()
rural_est_2022_census_tract_v2.rename(columns={'est_pop':'est_rural_pop_22_v2'}, inplace=True)
df_census_tract = df_census_tract.merge(rural_est_2022_census_tract_v2, on='id', how='left')
df_census_tract['diff_est_total_22_v2'] = df_census_tract['est_total_pop_22_v2'] - df_census_tract['total_pop_22']
df_census_tract['per_diff_est_total_22_v2'] = df_census_tract['diff_est_total_22_v2']/df_census_tract['total_pop_22']

df_rural_res = df_census_tract[['id', 'est_rural_pop_22_v2']].copy()
df_rural_res['est_rural_pop_22_v2'] = df_rural_res['est_rural_pop_22_v2'].fillna(0).round().astype(int)

print('Rural residents')
print(df_rural_res.head())

#################################################################################################################

# Find the covered populations - Individuals with a language barrier
lang_code = ['B06007_005M', 'B06007_008E']

lang_url = detailed_table + ','.join(lang_code) + geog
df_lang = pd.read_json(lang_url)
set_index(df_lang)

num_list = ['B06007_005M', 'B06007_008E']
df_lang[num_list] = df_lang[num_list].apply(pd.to_numeric)
df_lang['lang_pop'] = df_lang.iloc[:, 0:2].sum(axis=1)

df_lang['id'] = df_lang['state'] + df_lang['county'] + df_lang['tract']

df_lang_res = df_lang[['lang_pop', 'id']]

print('Individuals with a language barrier')
print(df_lang_res.head())

#################################################################################################################

# Find the covered populations - Individuals with incomes not exceeding 150 percent of poverty level
poverty_code = ['S1701_C01_040E']

poverty_url = subject_table + ','.join(poverty_code) + geog
df_poverty = pd.read_json(poverty_url)
set_index(df_poverty)

df_poverty.rename(columns={'S1701_C01_040E': 'poverty_pop'}, inplace=True)

df_poverty['id'] = df_poverty['state'] + df_poverty['county'] + df_poverty['tract']

df_poverty_res = df_poverty[['poverty_pop', 'id']]
print('Individuals with incomes not exceeding 150 percent of poverty level')
print(df_poverty_res.head())

# Merge the data frames
df_se2 = pd.merge(df_minority_res, df_lang_res, on='id', how='inner')
df_se2 = pd.merge(df_se2, df_poverty_res, on='id', how='inner')
df_se2 = pd.merge(df_se2, df_rural_res, on='id', how='inner')

df_se2[['total_pop', 'minority_pop', 'lang_pop', 'poverty_pop', 'est_rural_pop_22_v2']] = df_se2[['total_pop', 'minority_pop', 'lang_pop', 'poverty_pop', 'est_rural_pop_22_v2']].apply(pd.to_numeric)
df_se2['per_minority_pop'] = np.where(df_se2['total_pop'] > 0, df_se2['minority_pop'] / df_se2['total_pop'], 0)
df_se2['z_per_minority_pop'] = standardize_score(df_se2, 'per_minority_pop')

df_se2['per_lang_pop'] = np.where(df_se2['total_pop'] > 0, df_se2['lang_pop'] / df_se2['total_pop'], 0)
df_se2['z_per_lang_pop'] = standardize_score(df_se2, 'per_lang_pop')

df_se2['per_poverty_pop'] = np.where(df_se2['total_pop'] > 0, df_se2['poverty_pop'] / df_se2['total_pop'], 0)
df_se2['z_per_poverty_pop'] = standardize_score(df_se2, 'per_poverty_pop')

df_se2['per_est_rural_pop_22_v2'] = np.where(df_se2['total_pop'] > 0, df_se2['est_rural_pop_22_v2'] / df_se2['total_pop'], 0)
df_se2['z_per_est_rural_pop_22_v2'] = standardize_score(df_se2, 'per_est_rural_pop_22_v2')

df_se = pd.merge(df_se1, df_se2, on='id', how='inner')

# calculate SE score

df_se['SE'] = round(df_se['z_per_incar'] + df_se['z_per_vet'] + df_se['z_per_over60']
                    + df_se['z_per_dis'] + df_se['z_per_minority_pop'] + df_se['z_per_lang_pop']
                    + df_se['z_per_poverty_pop'] + df_se['z_per_est_rural_pop_22_v2'], 2)

df_se['SE_normed'] = 100*(df_se['SE']-df_se['SE'].min())/(df_se['SE'].max()-df_se['SE'].min())

df_se.to_csv('data/SE.csv', index=False)

