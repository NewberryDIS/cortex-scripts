import pandas as pd

edhs_assets = 'edhs_assets.csv'
edhs_cos = 'edhs_cos.csv'

df_assets = pd.read_csv(edhs_assets)
df_cos = pd.read_csv(edhs_cos)

df_cos['Parent Compound Object Identifier'] = df_cos['Unique identifier']

merged_df = df_assets.merge(df_cos, on='Parent Compound Object Identifier', how='inner')

# print(list(merged_df.columns))

merged_df = merged_df.dropna(axis=1, how='all')

merged_df.to_csv('edhs_assets_metadata.csv', encoding='utf-8-sig', index=False)