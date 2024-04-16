# # SE =  AGE60 + INCAR + VET + DIS + MIN + RURAL + LOWL + POV
# # 有需要的话大小写统一一下
# # 两个total pop是一个吗？如果不是，统一成一个
# # Maine 监狱人口总数为8700

import pandas as pd
import requests

detailed_table = 'https://api.census.gov/data/2022/acs/acs5?get='
subject_table = 'https://api.census.gov/data/2022/acs/acs5/subject?get='
geog = '&for=tract:*&in=state:23&in=county:*'

# B01001_001E: Total population of Maine
# B26103_004E: Incarcerated individuals
# B21001_002E: Veterans

key_detailed = ['B01001_001E','B26103_004E','B21001_002E']
url_detailed = detailed_table + ",".join(key_detailed) + geog
df_detailed = pd.read_json(url_detailed)

df_detailed.columns = df_detailed.iloc[0]
df_detailed = df_detailed[1:]

df_detailed.rename(columns={'B01001_001E': 'TOTALPOP'}, inplace=True)
df_detailed['TOTALPOP'] = pd.to_numeric(df_detailed['TOTALPOP'])

df_detailed['VET'] = pd.to_numeric(df_detailed['B21001_002E'], errors='coerce') / df_detailed['TOTALPOP']

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

df_detailed['INCAR'] = pd.to_numeric(df_detailed['B26103_004E'], errors='coerce')
num_tracts = df_detailed['tract'].nunique()
avg_incar_per_tract = incar / num_tracts
df_detailed['AVG_INCAR_PER_TRACT'] = avg_incar_per_tract
df_detailed['INCAR'] = df_detailed['AVG_INCAR_PER_TRACT'] / df_detailed['TOTALPOP']

# S0101_C01_028E: 60 years and over
# S1810_C02_001E: Disabled population

key_subject = ['S0101_C01_028E','S1810_C02_001E']
url_subject = subject_table + ",".join(key_subject) + geog
df_subject = pd.read_json(url_subject)

df_subject.columns = df_subject.iloc[0]  # Set the first row as column names
df_subject = df_subject[1:]  # Remove the first row (redundant column names)

# Calculate proportion of over 60 population and disabled population
df_subject['OVER60'] = pd.to_numeric(df_subject['S0101_C01_028E'], errors='coerce') / df_detailed['TOTALPOP']
df_subject['DIS'] = pd.to_numeric(df_subject['S1810_C02_001E'], errors='coerce') / df_detailed['TOTALPOP']

str_list = ['state', 'county', 'tract']
df_detailed['ID'] = df_detailed['state'] + df_detailed['county'] + df_detailed['tract']
df_subject['ID'] = df_subject['state'] + df_subject['county'] + df_subject['tract']
df_detailed_res = df_detailed[['ID', 'TOTALPOP', 'INCAR', 'VET']]
df_subject_res = df_subject[['ID', 'OVER60', 'DIS']]
df_se1 = pd.merge(df_detailed_res, df_subject_res, on='ID', how='inner')

df_se1['SE1'] = (df_se1['OVER60'] + df_se1['VET'] + df_se1['DIS'] + df_se1['INCAR']) * 100


########################################################################################
geog = '&for=tract:*&in=state:23&in=county:*'
subject_root = 'https://api.census.gov/data/2022/acs/acs5/subject?get='
detailed_root = 'https://api.census.gov/data/2022/acs/acs5?get='
profile_root = 'https://api.census.gov/data/2022/acs/acs5/profile?get='
cprofile_root = 'https://api.census.gov/data/2022/acs/acs5/cprofile?get='
responserate_root = 'https://api.census.gov/data/2020/dec/dhc/groups?get='

# reset the dataframe index
def set_index(df):
    df.columns = df.iloc[0]
    df.drop(index=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

# Find the covered populations - Members of a racial or ethnic minority group
minority_code = ['DP05_0072E', 'DP05_0073E', 'DP05_0080E', 'DP05_0081E', 'DP05_0082E',
                 'DP05_0083E', 'DP05_0084E', 'DP05_0085E']

minority_url = profile_root + ','.join(minority_code) + geog
df_minority = pd.read_json(minority_url)
set_index(df_minority)

num_list = ['DP05_0073E', 'DP05_0080E', 'DP05_0081E', 'DP05_0082E', 'DP05_0083E', 'DP05_0084E', 'DP05_0085E']
str_list = ['state', 'county', 'tract']
df_minority[num_list] = df_minority[num_list].apply(pd.to_numeric)
df_minority.rename(columns={'DP05_0072E': 'TOTAL_POP'}, inplace=True)
df_minority['MINORITY_POP'] = df_minority.iloc[:, 1:8].sum(axis=1)

# Create 'ID' column
df_minority['ID'] = df_minority['state'] + df_minority['county'] + df_minority['tract']

df_minority_res = df_minority[['TOTAL_POP', 'MINORITY_POP', 'ID']]

# Find the covered populations - Individuals with a language barrier
lang_code = ['B06007_005M', 'B06007_008E']

lang_url = detailed_root + ','.join(lang_code) + geog
df_lang = pd.read_json(lang_url)
set_index(df_lang)

num_list = ['B06007_005M', 'B06007_008E']
df_lang[num_list] = df_lang[num_list].apply(pd.to_numeric)
df_lang['LANG_POP'] = df_lang.iloc[:, 0:2].sum(axis=1)

# Create 'ID' column
df_lang['ID'] = df_lang['state'] + df_lang['county'] + df_lang['tract']

df_lang_res = df_lang[['LANG_POP', 'ID']]

# Find the covered populations - Individuals with incomes not exceeding 150 percent of poverty level
poverty_code = ['S1701_C01_040E']

poverty_url = subject_root + ','.join(poverty_code) + geog
df_poverty = pd.read_json(poverty_url)
set_index(df_poverty)

df_poverty.rename(columns={'S1701_C01_040E': 'POVERTY_POP'}, inplace=True)

# Create 'ID' column
df_poverty['ID'] = df_poverty['state'] + df_poverty['county'] + df_poverty['tract']

df_poverty_res = df_poverty[['POVERTY_POP', 'ID']]
# print('Individuals with incomes not exceeding 150 percent of poverty level')
# print(df_poverty_res.head())

# Merge the data frames
df_se2 = pd.merge(df_minority_res, df_lang_res, on='ID', how='inner')
df_se2 = pd.merge(df_se2, df_poverty_res, on='ID', how='inner')

df_se2[['POVERTY_POP', 'LANG_POP', 'MINORITY_POP', 'TOTAL_POP']] = df_se2[['POVERTY_POP', 'LANG_POP', 'MINORITY_POP', 'TOTAL_POP']].apply(pd.to_numeric)

# Calculate the SE score
df_se2['SE2'] = (df_se2['POVERTY_POP'] / df_se2['TOTAL_POP'] + df_se2['LANG_POP'] / df_se2['TOTAL_POP'] + df_se2['MINORITY_POP'] / df_se2['TOTAL_POP']) * 100

df_se2['SE'] = round(df_se1['SE1'] + df_se2['SE2'], 2)

print('Social Equity Score:')
print(df_se2[['ID', 'SE']])
