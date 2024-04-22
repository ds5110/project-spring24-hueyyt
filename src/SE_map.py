import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

url = "https://www2.census.gov/geo/tiger/TIGER2022/TRACT/tl_2022_23_tract.zip"
gdf = gpd.read_file(url)
gdf = gdf[gdf['ALAND'] > 0]

url = "https://www2.census.gov/geo/docs/reference/codes/files/st23_me_cousub.txt"
df = pd.read_csv(url, header=None, converters={"county": str}, usecols=[2, 3], names=["county", "name"])
df = df.drop_duplicates(subset="name")
df.set_index('county', inplace=True)
diction = df.to_dict(orient='index')

df_data = pd.read_csv('data/SE.csv')
df_data['county'] = df_data['id'].apply(lambda x: str(x)[2:5] + str(x)[-4:])
df_data['GEOID'] = df_data['id'].astype(str)
df_data.drop(columns=['id'], inplace=True)

scores = ['SE_normed', 'per_incar', 'per_vet', 'per_over60', 'per_dis', 'per_minority_pop', 'per_lang_pop', 'per_poverty_pop', 'per_est_rural_pop_22_v2']

for score in scores:
    df_data['title'] = df_data['county'].apply(lambda x: diction[x[:3]]['name'] + "\ntract:" + x[-4:] if x[:3] in diction else "N/A")
    df_data['title'] = df_data['title'] + "\n" + df_data[score].round(2).astype(str)

    new_gdf = gdf.merge(df_data[['GEOID', score, 'title']], on='GEOID', how='left')
    new_wm = new_gdf.to_crs(epsg=3857)

    # use percentiles to emphasize the relative ranking
    percentiles = np.percentile(new_gdf[score], np.arange(0, 101, 10))
    norm = mpl.colors.BoundaryNorm(boundaries=percentiles, ncolors=256)
    cmap = mpl.cm.RdYlGn_r
    ax = new_wm.plot(score, legend=True, norm=norm, cmap=cmap)
    new_wm.boundary.plot(ax=ax, linewidth=0.2, edgecolor='#333')
    plt.gcf().set_size_inches(10, 10)
    plt.title(label=score + " scores per census tract")
    plt.savefig('figs/'+score+'_tract.png', dpi=300)
    plt.show()
    plt.close()
    print("Plot saved to figs/" + score + "_tract.png \n")
