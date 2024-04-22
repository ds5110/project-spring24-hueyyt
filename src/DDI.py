import pandas as pd

# Load the INFA and SE scores for Maine
infa_df = pd.read_csv("data/infa_scaled.csv")
se_df = pd.read_csv("data/SE.csv")

# Merge the dataframes on the 'id' column
#maine_df = pd.merge(infa_df, se_df, on='id', how='inner')

infa_df['id'] = infa_df['id'].astype(str)
infa_df = infa_df.drop_duplicates(subset='id')
se_df['id'] = se_df['id'].astype(str)
maine_df = pd.merge(infa_df[['id', 'INFA_scaled']], se_df[['id', 'SE_normed']], on='id', how='inner')

# Calculate DDI as the sum of INFA_scaled and SE_normed scores
maine_df['DDI'] = maine_df['INFA_scaled'] + maine_df['SE_normed']

# Scale DDI scores to be within the range of 0 to 100
maine_df['DDI_scaled'] = 100 * (maine_df['DDI'] - maine_df['DDI'].min()) / (maine_df['DDI'].max() - maine_df['DDI'].min())

# Output the whole table
print(maine_df)

# Save the results to a CSV file
maine_df.to_csv("data/DDI.csv", index=False)
