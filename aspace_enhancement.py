import pandas as pd
import re

# Load the first spreadsheet with Ref ID and Folder columns
df_ref_folder = pd.read_csv('fullercontainer2.csv')

# Load the second spreadsheet with Original file name column
df_original = pd.read_csv('Fuller_enhancement_test.csv')

# def expand_range(range_str):
#     if re.match(r'^\d+-\d+$', range_str):
#         start, end = map(int, range_str.split('-'))
#         return list(range(start, end + 1))
#     elif re.match(r'^\d+$', range_str):
#         return [int(range_str)]
#     else:
#         return []

df_ref_folder['Folder'] = df_ref_folder['Folder'].astype(str)

# Create a new DataFrame by expanding the range in 'Folder'
expanded_rows = []
for index, row in df_ref_folder.iterrows():
    title = row['Title']
    ref_id = row['Ref ID']
    folder_range = row['Folder']
    
    if folder_range:
        if '-' in folder_range:
            start, end = folder_range.split('-')
            for folder_value in range(int(start), int(end) + 1):
                expanded_rows.append({'Title': title, 'Ref ID': ref_id, 'Folder': str(folder_value)})
        else:
            expanded_rows.append({'Title': title, 'Ref ID': ref_id, 'Folder': folder_range})

# Create the expanded DataFrame
expanded_df = pd.DataFrame(expanded_rows)

def remove_leading_zeroes(value):
    if value.isdigit():
        return str(int(value))
    return value

def extract_folder(file_name):
    parts = file_name.split('_')[7]
    parts_without_leading_zeroes = remove_leading_zeroes(parts)
    return parts_without_leading_zeroes

ref_id_mapping = {}

for index, row in df_original.iterrows():
    original_file_name = row['Original file name']
    folder_value = extract_folder(original_file_name)
    # print(folder_value)
    
    if folder_value is not None:
        matching_rows = expanded_df[expanded_df['Folder'] == folder_value]
        
        if not matching_rows.empty:
            ref_id = matching_rows.iloc[0]['Ref ID']
            ref_id_mapping[index] = ref_id

df_original['Ref ID'] = df_original.index.map(ref_id_mapping)

# Merge the dataframes based on 'Ref ID'
merged_df = pd.merge(df_original, df_ref_folder, on='Ref ID', how='left')

# Drop selected columns
columns_to_drop = ['Title_x', 'Folder', 'Resource Title', 'EAD ID', 'Identifier', 'Box']

merged_df.drop(columns=columns_to_drop, inplace=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('merged_csv.csv', index=False)