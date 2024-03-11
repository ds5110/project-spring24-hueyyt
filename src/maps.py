import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 读取地理数据
url = "https://www2.census.gov/geo/tiger/TIGER2022/TRACT/tl_2022_23_tract.zip"
gdf = gpd.read_file(url, converters={"GEOID": int})
gdf = gdf[gdf['ALAND'] > 0]

# 读取县级行政单位名称数据
url = "https://www2.census.gov/geo/docs/reference/codes/files/st23_me_cousub.txt"
df = pd.read_csv(url, header=None, converters={"county": str}, usecols=[2, 3], names=["county", "name"])
df = df.drop_duplicates(subset="name")
df.set_index('county', inplace=True)
diction = df.to_dict(orient='index')

# 读取 INFA 分数数据
score = 'INFA_scaled'
df_data = pd.read_csv('data/infa_scaled.csv', index_col=None)

print(df_data.columns)

del df_data[df_data.columns[0]]
df_data['county'] = df_data['tract'].apply(lambda x: str(x)[2:5] + str(x)[-4:])
df_data['title'] = df_data['county'].apply(lambda x: diction[x[:3]]['name'] + "\ntract:" + x[-4:] if x[:3] in diction else NA)
df_data['title'] = df_data['title'] + "\n" + round(df_data[score], 2).astype(str)
df_data['GEOID'] = df_data['tract'].astype(str)
df_data.drop(columns=['tract'], inplace=True)

# 合并地理数据和 INFA 分数
new_gdf = gdf.merge(df_data[['GEOID', score, 'title']], on='GEOID', how='left')
new_gdf.to_file('docs/'+score+'.json', driver="GeoJSON")
print('Saving '+score+' GeoJSON data to docs/'+score+'.json')

# 绘制 INFA 分数地图
new_wm = new_gdf.to_crs(epsg=3857)
print('Plotting ' + score + ' scores on map')
bounds = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=256)
cmap = mpl.cm.RdYlGn_r
ax = new_wm.plot(score, legend=True, norm=norm, cmap=cmap)
new_wm.boundary.plot(ax=ax, linewidth=0.2, edgecolor='#333')
plt.gcf().set_size_inches(10, 10)
plt.title(label=score + " scores per census tract")
plt.savefig('img/'+score+'_tract.png', dpi=300)
plt.show()
print("Plot saved to img/" + score + "_tract.png \n")
plt.close()
