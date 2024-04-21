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

total_covered_state_url = 'https://www2.census.gov/programs-surveys/demo/datasets/community-resilience/state_total_covered_populations_2022.xlsx'
total_covered_tract_url = 'https://www2.census.gov/programs-surveys/demo/datasets/community-resilience/county_tract_total_covered_populations.xlsx'

#################################################################################################################
# Find the covered populations - Incarcerated individuals and Veterans
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

df_total_covered_state = pd.read_excel(total_covered_state_url, sheet_name='state_total_covered_populations', dtype={'geography_name': str})
maine_row = df_total_covered_state[df_total_covered_state['st'] == 23]
if not maine_row.empty:
    me_totalpop = maine_row['state_tot_pop'].values[0]
    pct_incarc_pop = maine_row['pct_incarc_pop'].values[0]
else:
    print("Maine data not found in the DataFrame.")

state_incar = (me_totalpop * (pct_incarc_pop/100)).round().astype(int)

df_detailed['proportion'] = df_detailed['totalpop'] / me_totalpop
# Estimate the number of incarcerated individuals in each tract based on the proportion
df_detailed['estimated_incar'] = df_detailed['proportion'] * state_incar
# Round the estimated incarcerated individuals to the nearest integer
df_detailed['estimated_incar'] = df_detailed['estimated_incar'].round().astype(int)
df_detailed['per_incar'] = np.where(df_detailed['totalpop'] > 0, df_detailed['estimated_incar'] / df_detailed['totalpop'], 0)
df_detailed['z_per_incar'] = standardize_score(df_detailed, 'per_incar')

#################################################################################################################
# Find the covered populations - Persons who are 60 years of age or older and persons with disabilities
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
df_detailed_res = df_detailed[['id', 'totalpop', 'estimated_incar', 'per_incar', 'z_per_incar','vet', 'per_vet', 'z_per_vet']]
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

#################################################################################################################
# Find the covered populations - Rural residents

df_rural_res = pd.read_csv('data/rural_est.csv')
df_rural_res['id'] = df_rural_res['id'].astype(str)


#################################################################################################################

# Find the covered populations - Individuals with a language barrier
# lang_code = ['B06007_005M', 'B06007_008E']

# lang_url = detailed_table + ','.join(lang_code) + geog
# df_lang = pd.read_json(lang_url)
# set_index(df_lang)

# num_list = ['B06007_005M', 'B06007_008E']
# df_lang[num_list] = df_lang[num_list].apply(pd.to_numeric)
# df_lang['lang_pop'] = df_lang.iloc[:, 0:2].sum(axis=1)

# df_lang['id'] = df_lang['state'] + df_lang['county'] + df_lang['tract']

# df_lang_res = df_lang[['id', 'lang_pop']]


lang_pop_state = maine_row['lang_barrier_pop'].values[0]
pct_lang_pop_state = maine_row['pct_lang_barrier_pop'].values[0]

df_lang = df_minority[['id', 'total_pop']].copy()
df_lang['total_pop'] = df_lang['total_pop'].astype(int)
df_lang['rate_tract_state'] = df_lang['total_pop'] / me_totalpop
df_lang['estimated_lang'] = df_lang['rate_tract_state'] * lang_pop_state
df_lang['estimated_lang'] = df_lang['estimated_lang'].round().astype(int)
df_lang_res = df_lang[['id', 'estimated_lang']]

#################################################################################################################

# Find the covered populations - Individuals with incomes not exceeding 150 percent of poverty level
poverty_code = ['S1701_C01_040E']

poverty_url = subject_table + ','.join(poverty_code) + geog
df_poverty = pd.read_json(poverty_url)
set_index(df_poverty)

df_poverty.rename(columns={'S1701_C01_040E': 'poverty_pop'}, inplace=True)

df_poverty['id'] = df_poverty['state'] + df_poverty['county'] + df_poverty['tract']

df_poverty_res = df_poverty[['id', 'poverty_pop']]

# assign location name
rural_url = responserate_table + geog_rural
rural_response = requests.get(rural_url)
rural_data = rural_response.json()
df_rural_20 = pd.DataFrame(rural_data)
set_index(df_rural_20)
df_rural_20.rename(columns={'GEO_ID': 'geo_id'}, inplace=True)
df_rural_20['geo_id'] = df_rural_20['geo_id'].astype(str)
df_rural_20['id'] = df_rural_20['geo_id'].apply(lambda x: x.split("US")[1][:-4])
df_rural_20['loc'] = df_rural_20['NAME'].str.extract(r'(Census Tract \d+(?:\.\d+)?, \w+ County)')
df_loc = df_rural_20[['loc', 'id']].copy()
df_loc = df_loc.drop_duplicates(subset=['id', 'loc'])

# Merge the data frames
df_se2 = pd.merge(df_minority_res, df_lang_res, on='id', how='inner')
df_se2 = pd.merge(df_se2, df_poverty_res, on='id', how='inner')
df_se2 = pd.merge(df_se2, df_rural_res, on='id', how='inner')

df_se2[['total_pop', 'minority_pop', 'estimated_lang', 'poverty_pop', 'est_rural_pop_22_v2']] = df_se2[['total_pop', 'minority_pop', 'estimated_lang', 'poverty_pop', 'est_rural_pop_22_v2']].apply(pd.to_numeric)
df_se2['per_minority_pop'] = np.where(df_se2['total_pop'] > 0, df_se2['minority_pop'] / df_se2['total_pop'], 0)
df_se2['z_per_minority_pop'] = standardize_score(df_se2, 'per_minority_pop')

df_se2['per_lang_pop'] = np.where(df_se2['total_pop'] > 0, df_se2['estimated_lang'] / df_se2['total_pop'], 0)
df_se2['z_per_lang_pop'] = standardize_score(df_se2, 'per_lang_pop')

df_se2['per_poverty_pop'] = np.where(df_se2['total_pop'] > 0, df_se2['poverty_pop'] / df_se2['total_pop'], 0)
df_se2['z_per_poverty_pop'] = standardize_score(df_se2, 'per_poverty_pop')

df_se2['per_est_rural_pop_22_v2'] = np.where(df_se2['total_pop'] > 0, df_se2['est_rural_pop_22_v2'] / df_se2['total_pop'], 0)
df_se2['z_per_est_rural_pop_22_v2'] = standardize_score(df_se2, 'per_est_rural_pop_22_v2')

df_se = pd.merge(df_se1, df_se2, on='id', how='inner')
df_se = pd.merge(df_se, df_loc, on='id', how='inner')

# calculate SE score

df_se['SE'] = df_se['z_per_incar'] + df_se['z_per_vet'] + df_se['z_per_over60'] + df_se['z_per_dis'] + df_se['z_per_minority_pop'] + df_se['z_per_lang_pop'] + df_se['z_per_poverty_pop'] + df_se['z_per_est_rural_pop_22_v2']

df_se['SE_normed'] = 100*(df_se['SE']-df_se['SE'].min())/(df_se['SE'].max()-df_se['SE'].min())

# drop column
df_se = df_se.drop(columns=['total_pop'])

# check top census tracts
df_se_top = df_se[['SE_normed', 'loc']].sort_values(by='SE_normed', ascending = False, inplace=False)
df_vet_res_top = df_se[['vet', 'SE_normed', 'loc']].sort_values(by='vet', ascending = False, inplace=False)
df_incar_res_top = df_se[['estimated_incar', 'SE_normed', 'loc']].sort_values(by='estimated_incar', ascending = False, inplace=False)
df_over60_res_top = df_se[['over60', 'SE_normed', 'loc']].sort_values(by='over60', ascending = False, inplace=False)
df_dis_res_top = df_se[['dis', 'SE_normed', 'loc']].sort_values(by='dis', ascending = False, inplace=False)
df_minority_res_top = df_se[['minority_pop', 'SE_normed', 'loc']].sort_values(by='minority_pop', ascending = False, inplace=False)
df_rural_res_top = df_se[['est_rural_pop_22_v2', 'SE_normed', 'loc']].sort_values(by='est_rural_pop_22_v2', ascending = False, inplace=False)
df_lang_res_top = df_se[['estimated_lang', 'SE_normed', 'loc']].sort_values(by='estimated_lang', ascending = False, inplace=False)
df_poverty_res_top = df_se[['poverty_pop', 'SE_normed', 'loc']].sort_values(by='poverty_pop', ascending = False, inplace=False)

print('Top census tracts')
print('SE scores')
print(df_se_top.head())

print('Persons who are 60 years of age or older')
print(df_over60_res_top.head())

print('Incarcerated individuals')
print(df_incar_res_top.head())

print('Veterans')
print(df_vet_res_top.head())

print('Persons with disabilities')
print(df_dis_res_top.head())

print('Members of a racial or ethnic minority group')
print(df_minority_res_top.head())

print('Rural residents')
print(df_rural_res_top.head())

print('Individuals with a language barrier')
print(df_lang_res_top.head())

print('Individuals with incomes not exceeding 150 percent of poverty level')
print(df_poverty_res_top.head())
df_se.to_csv('data/SE.csv', index=False)
