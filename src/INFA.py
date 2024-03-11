import pandas as pd

# 假设已经按照您的文件格式和路径读取数据
speed_df = pd.read_csv("data/speed.txt", delimiter='\t')
population_df = pd.read_csv("data/population.txt", delimiter='\t')

# 转换 'tract' 和 'geo_id' 列的数据类型为字符串，以便合并
speed_df['tract'] = speed_df['tract'].astype(str)
population_df['geo_id'] = population_df['geo_id'].astype(str)

# 合并数据集
merged_df = pd.merge(speed_df, population_df, left_on='tract', right_on='geo_id', how='inner')

# 确保 'pct_no_bb_or_computer_pop', 'mean_max_advertised_download_speed' 和 'mean_max_advertised_upload_speed' 列是数值类型
merged_df['pct_no_bb_or_computer_pop'] = pd.to_numeric(merged_df['pct_no_bb_or_computer_pop'])
merged_df['mean_max_advertised_download_speed'] = pd.to_numeric(merged_df['mean_max_advertised_download_speed'])
merged_df['mean_max_advertised_upload_speed'] = pd.to_numeric(merged_df['mean_max_advertised_upload_speed'])

# 计算 NIA 和 NCD 值
merged_df['NIA'] = merged_df['pct_no_bb_or_computer_pop'] / 2
merged_df['NCD'] = merged_df['pct_no_bb_or_computer_pop'] / 2

# 标准化 DNS 和 UPS 数据
merged_df['DNS'] = merged_df['mean_max_advertised_download_speed'] / merged_df['mean_max_advertised_download_speed'].max() * 100
merged_df['UPS'] = merged_df['mean_max_advertised_upload_speed'] / merged_df['mean_max_advertised_upload_speed'].max() * 100

# 计算 INFA 得分
merged_df['INFA'] = merged_df['NIA'] * 0.35 + merged_df['NCD'] * 0.35 - merged_df['DNS'] * 0.15 - merged_df['UPS'] * 0.15

# 缩放 INFA 分数到 0 到 100 的范围
merged_df['INFA_scaled'] = 100 * (merged_df['INFA'] - merged_df['INFA'].min()) / (merged_df['INFA'].max() - merged_df['INFA'].min())

# 输出结果
print(merged_df[['tract', 'INFA_scaled']])

# 保存到 CSV 文件

merged_df[['tract', 'INFA_scaled']].to_csv("data/infa_scaled.csv")
