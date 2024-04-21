# Find the covered populations - Rural residents

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

geog = '&for=tract:*&in=state:23&in=county:*'
geog_rural = '&for=block:*&in=state:23+county:*+tract:*'
responserate_table = 'https://api.census.gov/data/2020/dec/dhc?get=group(P2)'
profile_table = 'https://api.census.gov/data/2022/acs/acs5/profile?get='


total_covered_state_url = 'https://www2.census.gov/programs-surveys/demo/datasets/community-resilience/state_total_covered_populations_2022.xlsx'
total_covered_tract_url = 'https://www2.census.gov/programs-surveys/demo/datasets/community-resilience/county_tract_total_covered_populations.xlsx'

rural_url = responserate_table + geog_rural
rural_response = requests.get(rural_url)
rural_data = rural_response.json()
df_rural_20 = pd.DataFrame(rural_data)
set_index(df_rural_20)

total_code = ['DP05_0072E']
total_url = profile_table + ','.join(total_code) + geog
df_total = pd.read_json(total_url)
set_index(df_total)

df_total['DP05_0072E'] = df_total['DP05_0072E'].apply(pd.to_numeric)
df_total.rename(columns={'DP05_0072E': 'total_pop'}, inplace=True)
df_total['id'] = df_total['state'] + df_total['county'] + df_total['tract']

# data preprocessing
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

# check if we can use block to assign rural/urban
urban_rural_pop_bool = len(df_rural_20[(df_rural_20['urban_pop'] != 0) & (df_rural_20['rural_pop'] != 0)])
not_defined_pop_bool = len(df_rural_20[df_rural_20['not_defined'] != 0])
if urban_rural_pop_bool == 0 and not_defined_pop_bool == 0:
  print('Block level data can be used to assign rural/urban labels.')

# assign rural labels to blocks
df_rural_20['rural'] = np.where((df_rural_20['total_pop'] == df_rural_20['urban_pop']) & (df_rural_20['total_pop'] != 0), 0,
                              np.where((df_rural_20['total_pop'] == df_rural_20['rural_pop']) & (df_rural_20['total_pop'] != 0), 1, None))

# estimate 2022 rural residents based on state data
df_total_covered_state = pd.read_excel(total_covered_state_url, sheet_name='state_total_covered_populations', dtype={'geography_name': str})
maine_row = df_total_covered_state[df_total_covered_state['st'] == 23]
me_totalpop = maine_row['state_tot_pop'].values[0]
rural_pop_state = maine_row['rural_pop'].values[0]
pct_rural_pop_state = maine_row['pct_rural_pop'].values[0]

df_rural_v1 = df_total[['id', 'total_pop']].copy()
df_rural_v1['total_pop'] = df_rural_v1['total_pop'].astype(int)
df_rural_v1['rate_tract_state'] = df_rural_v1['total_pop'] / me_totalpop
df_rural_v1['estimated_rural_v1'] = df_rural_v1['rate_tract_state'] * rural_pop_state
df_rural_v1['estimated_rural_v1'] = df_rural_v1['estimated_rural_v1'].round().astype(int)
df_rural_res = df_rural_v1[['id', 'estimated_rural_v1']]

# estimate 2022 rural residents based on 2020 data
df_est = df_rural_20.copy()
df_census_tract_20 = df_est.groupby('id')['total_pop'].sum().reset_index()
df_census_tract_20.rename(columns={'total_pop': 'total_pop_20'}, inplace=True)

df_census_tract_22 = df_total.copy()
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

temp = df_census_tract[['id', 'est_rural_pop_22_v2']].copy()
temp['est_rural_pop_22_v2'] = temp['est_rural_pop_22_v2'].fillna(0).round().astype(int)
df_rural_res = pd.merge(df_rural_res, temp, how='inner', on='id')

# estimate 2022 rural residents based on census tract 2019
df_total_covered_tract = pd.read_excel(total_covered_tract_url, sheet_name='tract_total_covered_populations', dtype={'geography_name': str})
df_total_covered_tract['geo_id'] = df_total_covered_tract['geo_id'].astype(str)
df_total_covered_tract.rename(columns={'geo_id': 'id'}, inplace=True)
df_total_covered_tract['st'] = df_total_covered_tract['id'].str[:2]
maine = df_total_covered_tract[df_total_covered_tract['st'] == '23']
df_rural_v3_temp = maine[['id', 'pct_rural_pop']].copy()
total_temp = df_total[['id', 'total_pop']].copy()

df_rural_v3 = pd.merge(total_temp, df_rural_v3_temp, how='left', on='id')
df_rural_v3 = df_rural_v3.replace('(X)', 0).fillna(0)
df_rural_v3['total_pop'] = df_rural_v3['total_pop'].astype(int)
df_rural_v3['est_rural_pop_v3'] = df_rural_v3['total_pop'] * (df_rural_v3['pct_rural_pop'] / 100).round().astype(int)
df_rural_res = pd.merge(df_rural_res, df_rural_v3[['id', 'est_rural_pop_v3']], how='inner', on='id')

print('Total rural population in maine (actual):\n', rural_pop_state)
print('Total rural population in maine (estimation v1):\n', df_rural_res['estimated_rural_v1'].sum())
print('Total rural population in maine (estimation v2):\n', df_rural_res['est_rural_pop_22_v2'].sum())
print('Total rural population in maine (estimation v3):\n', df_rural_res['est_rural_pop_v3'].sum())

df_rural_res.to_csv('data/rural_est.csv', index=False)
