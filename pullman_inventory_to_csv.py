import re
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('Cortex_CSV', nargs='?', help='CSV of Cortex Unique IDS and filenames')
parser.add_argument('Pullman_CSV', nargs='?', help='CSV of Pullman Inventory')
args = parser.parse_args()

# Title is: First Name Last Name, Pullman Company employee service records, Birth Year
def process_titles(row):
    first_name = row['First Name on Card']
    last_name = row['Last Name on Card']
    birth_year = row['Birth Year']
   
    if  not pd.isna(birth_year):
        title = f"{first_name} {last_name} (born {birth_year}), Pullman Company - Chicago, Porters"
    else:
        title = f"{first_name} {last_name}, Pullman Company - Chicago, Porters"
    return title

def call_number_finalize(row):
    box_number = row['Box']
    folder_number = row['Folder']
   
    call_number = f"Case Pullman 06/02/03 Box {box_number} Folder {folder_number}"

    return call_number

def birth_place(row):
    birth_state = row['Birth State']
    birth_city = row['Birth City']

    if not pd.isna(birth_state):
        description = f"Born in {birth_city}, {birth_state}"
    else:
        description = ''
   
    return description

pullman_inventory_csv = args.Pullman_CSV
cortex_csv = args.Cortex_CSV

pullman_df = pd.read_csv(pullman_inventory_csv)
cortex_df = pd.read_csv(cortex_csv)

# Extract the folder number from the file name
folder_number_cortex = r'fl_0*(\d+)_'
cortex_df['Folder'] = cortex_df['Original file name'].str.extract(folder_number_cortex).astype(int)

# print(cortex_df['Folder'])
# print(pullman_df['Folder'])

merged_df = cortex_df.merge(pullman_df, on='Folder', how='inner')

merged_df['Title'] = merged_df.apply(process_titles, axis=1)

merged_df['Description'] = merged_df.apply(birth_place, axis=1)

merged_df['Call Number'] = merged_df.apply(call_number_finalize, axis=1)

merged_df['Format'] = 'Personnel records'
merged_df['Archival Collection Title'] = 'Pullman Company records'
merged_df['Contributing Institution'] = 'Newberry Library'
merged_df['Newberry Open Access Policy'] = "The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to <a href='https://www.newberry.org/policies#open-access' target='_blank'>these terms and conditions.</a>"
merged_df['BibID'] = '991194448805867'
merged_df['Finding Aid'] = '<a href="https://archives.newberry.org/repositories/2/resources/1152" target="_blank">View finding aid</a>|<a href="https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma991194448805867" target="_blank">View record</a>'


merged_df.to_csv('Pullman_test.csv', index=False)