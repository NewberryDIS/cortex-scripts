import pandas as pd
import argparse
import math
import csv

parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of Novacco-FAST Dictionary')
parser.add_argument('csv2', nargs='?', help='CSV of Novacco metadata')
args = parser.parse_args()

# Load the replacement dictionary CSV into a DataFrame
dict_csv_path = args.csv1
df_dict = pd.read_csv(dict_csv_path, encoding='utf-8-sig')

# Create a replacement dictionary from the DataFrame
replacement_dict = dict(zip(df_dict['SUBJECTS'], df_dict['Subject Conversion']))

# Load the data to be updated CSV into another DataFrame
data_csv_path = args.csv2
df_data = pd.read_csv(data_csv_path, encoding='utf-8-sig')
df_data['SUBJECTS'] = df_data['SUBJECTS'].apply(lambda x: '' if pd.isna(x) or (isinstance(x, float) and math.isnan(x)) else str(x))

# # Iterate through the DataFrame and update multi-value fields
for index, row in df_data.iterrows():
    # print(row['SUBJECTS'])
    try:
        subjects = row['SUBJECTS'].split('|')
    except Exception as e:
        print(f'Error processing value {row["SUBJECTS"]}: {e}')
    
    updated_subjects = []
    for subject in subjects:
        if not isinstance(subject, float) or not math.isnan(subject):
            updated_subject = replacement_dict.get(subject)
            if updated_subject is not None:
                    updated_subjects.append(updated_subject)
            else:
                updated_subjects.append(subject)
        else:
            updated_subjects.append(subject)
        updated_subjects = [str(item).strip() for item in updated_subjects]
        try:        
            df_data.at[index, 'SUBJECTS'] = '|'.join(updated_subjects)
        except Exception as e:
            print(f"An error occured while joining subjects: {updated_subjects}: {e}")

# Code written for debugging float error
    # subjects = row['SUBJECTS'].split('|')  # Assuming values are pipe-separated
    
    # print(f"Original subjects: {subjects}")  # Print the original subjects
    
    # updated_subjects = []
    # for subject in subjects:
    #     updated_subject = replacement_dict.get(subject, subject)
    #     updated_subjects.append(updated_subject)
    #     print(f"Processing subject: {subject}, Updated subject: {updated_subject}")
    
    # try:
    #     df_data.at[index, 'SUBJECTS'] = '|'.join(updated_subjects)
    # except:
    #     print("An error occred wile joining subjects.")
    
    # print(f"Updated subjects: {updated_subjects}")  # Print the updated subjects

# Create a column mapping in original DataFrame
mapping_dict = dict(zip(df_dict['Subject Conversion'], df_dict['New Field']))
# print(mapping_dict)

for column in df_dict['New Field']:
    df_data['Format'] = ''
    df_data['Place'] = ''
    df_data['Subject'] = ''
    df_data['Not a heading'] = ''

# Iterate through the data DataFrame and move values to new columns
for index, row in df_data.iterrows():
    values = row['SUBJECTS'].split('|')
    
    for value in values:
        target_column = mapping_dict.get(value)
    
        if target_column is not None and target_column in df_data.columns:
            current_value = df_data.at[index, target_column]
            if current_value:
                df_data.at[index, target_column] = f"{current_value}|{value}"
            else:
                df_data.at[index, target_column] = value

columns_to_keep = ['FILENAME', 'Format', 'Place', 'Subject']

final_df = df_data[columns_to_keep]

# Save the modified DataFrame back to a new CSV file
output_path = 'modified_data.csv'
final_df.to_csv(output_path, index=False, encoding='utf-8-sig', errors='ignore')