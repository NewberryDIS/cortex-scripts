import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='csv to merge 1')
parser.add_argument('csv2', nargs='?', help='csv to merge 2')
args = parser.parse_args()

# Create DataFrame
df1 = pd.read_csv(args.csv1)
df2 = pd.read_csv(args.csv2)

# print(df1.columns)
# print(df2.columns)

# Perform an outer merge to keep all rows from both DataFrames
merged_df = pd.merge(df1, df2, left_on='Call Number', right_on='CALL_NUMBER', how='outer', suffixes=('_left', '_right'))

# Create the Link2 column based on the merged DataFrame
merged_df['Link2'] = merged_df['Link to view in Cortex']

# Select relevant columns
result_df = merged_df[['Call Number', 'CALL_NUMBER', 'Link2']]

# Save the resulting DataFrame to a CSV file
result_df.to_csv('merged_columns.csv', encoding='utf-8-sig', index=False)