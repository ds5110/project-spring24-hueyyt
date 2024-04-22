import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

# INFA scores
df_infa = pd.read_csv('data/infa_scaled.csv')
df_infa = df_infa.drop_duplicates(subset='id')
df_infa_top = df_infa[['id', 'INFA_scaled']].sort_values(by='INFA_scaled', ascending = False, inplace=False)
print('Top 5 census tracts with the highest infa score:\n')
print(df_infa_top.head())

# SE scores
df_se = pd.read_csv('data/SE.csv')
print(df_se.info())

# check top census tracts
df_vet_res_top = df_se[['vet', 'SE_normed', 'loc']].sort_values(by='vet', ascending = False, inplace=False)
df_incar_res_top = df_se[['estimated_incar', 'SE_normed', 'loc']].sort_values(by='estimated_incar', ascending = False, inplace=False)
df_over60_res_top = df_se[['over60', 'SE_normed', 'loc']].sort_values(by='over60', ascending = False, inplace=False)
df_dis_res_top = df_se[['dis', 'SE_normed', 'loc']].sort_values(by='dis', ascending = False, inplace=False)
df_minority_res_top = df_se[['minority_pop', 'SE_normed', 'loc']].sort_values(by='minority_pop', ascending = False, inplace=False)
df_rural_res_top = df_se[['est_rural_pop_22_v2', 'SE_normed', 'loc']].sort_values(by='est_rural_pop_22_v2', ascending = False, inplace=False)
df_lang_res_top = df_se[['estimated_lang', 'SE_normed', 'loc']].sort_values(by='estimated_lang', ascending = False, inplace=False)
df_poverty_res_top = df_se[['poverty_pop', 'SE_normed', 'loc']].sort_values(by='poverty_pop', ascending = False, inplace=False)


def compare_sets(top):

    over60_top = df_over60_res_top.head(top)['loc'].values
    incar_top = df_incar_res_top.head(top)['loc'].values
    vet_top = df_vet_res_top.head(top)['loc'].values
    dis_top = df_dis_res_top.head(top)['loc'].values
    minority_top = df_minority_res_top.head(top)['loc'].values
    rural_top = df_rural_res_top.head(top)['loc'].values
    lang_top = df_lang_res_top.head(top)['loc'].values
    poverty_top = df_poverty_res_top.head(top)['loc'].values

    dup_dict = {
        'Over 60': over60_top,
        'Incarcerated': incar_top,
        'Veterans': vet_top,
        'Disabled': dis_top,
        'Minority': minority_top,
        'Rural': rural_top,
        'Language': lang_top,
        'Poverty': poverty_top
    }
    keys = list(dup_dict.keys())
    results = {}
    print(f'\nTop {top} Comparison')
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            key1, key2 = keys[i], keys[j]
            set1 = set(dup_dict[key1])
            set2 = set(dup_dict[key2])
            common = set1.intersection(set2)
            if common:
                results[(key1, key2)] = common
                if len(common) >= top/2:
                    print('------------------------------------------')
                    print(f"{len(common)} common locations between {key1} and {key2}")
    return results

common_results_5 = compare_sets(5)
common_results_10 = compare_sets(10)
common_results_50 = compare_sets(50)



