import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# set url variables
geog = '&for=tract:*&in=state:23&in=county:*'
subject_root = 'https://api.census.gov/data/2022/acs/acs5/subject?get='
detailed_root = 'https://api.census.gov/data/2022/acs/acs5?get='
profile_root = 'https://api.census.gov/data/2022/acs/acs5/profile?get='
cprofile_root = 'https://api.census.gov/data/2022/acs/acs5/cprofile?get='
responserate_root = 'https://api.census.gov/data/2020/dec/dhc?get=group(H2)'

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
df_minority['ID'] = df_minority['state'] + df_minority['county'] + df_minority['tract']

df_minority_res = df_minority[['TOTAL_POP', 'MINORITY_POP', 'ID']]
print('Members of a racial or ethnic minority group')
print(df_minority_res.head())

# Find the covered populations - Rural residents
rural_url = responserate_root + geog
df_rural = pd.read_json(rural_url)
set_index(df_rural)

df_rural = df_rural.drop(columns=['H2_001NA', 'H2_002NA', 'H2_003NA', 'H2_004N', 'H2_004NA'])
df_rural.rename(columns={'H2_001N': 'TOTAL_POP'}, inplace=True)
df_rural.rename(columns={'H2_002N': 'URBAN_POP'}, inplace=True)
df_rural.rename(columns={'H2_003N': 'RURAL_POP'}, inplace=True)
df_rural['ID'] = df_rural['state'] + df_rural['county'] + df_rural['tract']

df_rural_res = df_rural[['NAME', 'TOTAL_POP', 'URBAN_POP', 'RURAL_POP', 'ID']]
print('Rural residents')
print(df_rural_res.head())

# Find the covered populations - Individuals with a language barrier
lang_code = ['B06007_005M', 'B06007_008E']

lang_url = detailed_root + ','.join(lang_code) + geog
df_lang = pd.read_json(lang_url)
set_index(df_lang)

num_list = ['B06007_005M', 'B06007_008E']
df_lang[num_list] = df_lang[num_list].apply(pd.to_numeric)
df_lang['LANG_POP'] = df_lang.iloc[:, 0:2].sum(axis=1)
df_lang['ID'] = df_lang['state'] + df_lang['county'] + df_lang['tract']

df_lang_res = df_lang[['LANG_POP', 'ID']]
print('Individuals with a language barrier')
print(df_lang_res.head())

# Find the covered populations - Individuals with incomes not exceeding 150 percent of poverty level
poverty_code = ['S1701_C01_040E']

poverty_url = subject_root + ','.join(poverty_code) + geog
df_poverty = pd.read_json(poverty_url)
set_index(df_poverty)

df_poverty.rename(columns={'S1701_C01_040E': 'POVERTY_POP'}, inplace=True)
df_poverty['ID'] = df_poverty['state'] + df_poverty['county'] + df_poverty['tract']

df_poverty_res = df_poverty[['POVERTY_POP', 'ID']]
print('Individuals with incomes not exceeding 150 percent of poverty level')
print(df_poverty_res.head())

# Merge the data frames and save the data
df = pd.merge(df_minority_res, df_lang_res, on='ID', how='inner')
df = pd.merge(df, df_poverty_res, on='ID', how='inner')
df[['TOTAL_POP', 'POVERTY_POP']] = df[['TOTAL_POP', 'POVERTY_POP']].apply(pd.to_numeric)
print('The covered populations - last four groups')
print('Number of unique ID:', df['ID'].nunique())
print(df.info())
print(df.head())

# Create a scatterplot to show the distribution
df_viz = df.copy()
df_viz = df_viz.drop(columns=['TOTAL_POP'])
sns.pairplot(df_viz)
plt.savefig('img/covered_pop_last_4_scatter.png')
plt.show()