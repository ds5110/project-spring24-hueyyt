import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## 算SE
## 合并readme和 Makefile
# Chosen two tables
detailed_table = 'https://api.census.gov/data/2022/acs/acs5?get='
subject_table = 'https://api.census.gov/data/2022/acs/acs5/subject?get='
geog = '&for=tract:*&in=state:23&in=county:*'

# B01001_001E: Total population of Maine
# B26103_004E: Incarcerated individuals
# B21001_002E: Veterans

key = ['B01001_001E','B26103_004E','B21001_002E']
url = detailed_table + ",".join(key) + geog
df_detailed = pd.read_json(url)

df_detailed.rename(columns={'B01001_001E': 'Total Pop'}, inplace = True)
df_detailed.rename(columns={'B26103_004E': 'Incarcerated Individuals'}, inplace = True)
df_detailed.rename(columns={'B21001_002E': 'Veterans'}, inplace = True)

#Output the first 5 rows of data
print(df_detailed.head())

# S0101_C01_028E: 60 years and over
# S1810_C02_001E: Disabled population

key = ['S0101_C01_028E','S1810_C02_001E']
url = subject_table + ",".join(key) + geog
df_subject = pd.read_json(url)

df_subject.rename(columns={'S0101_C01_028E': 'Over 60 Pop'})
df_subject.rename(columns={'S1810_C01_001E': 'Disabled'})

#Output the first 5 rows of data
print(df_subject.head())

