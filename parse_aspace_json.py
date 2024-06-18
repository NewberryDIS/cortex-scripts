
import csv
import json
import requests
import pandas as pd
import re
import argparse
from datetime import date
import time
from bs4 import BeautifulSoup

curYear = date.today().year
today = str(date.today())

parser = argparse.ArgumentParser()
parser.add_argument('Cortex_CSV', nargs='?', help='CSV of Cortex Unique IDS and filenames')
args = parser.parse_args()

# changes titles so that they contain folder, archival collection title, series, and date i.e., "Abbeville's Tides, typed draft, Jack Fuller works, 2000"
def process_titles(row):
    title = row['Title_Aspace']
    arch_coll_title = row['Archival Collection Title']
    series = row['Series Name']
    date = row['Created Date']

    if title[0].islower() and '-' in title:
        title_split = title.split(' - ')
        final_title = title_split[1][0].capitalize() + title_split[1][1:]
        seriesinfo_in_title = title_split[0]
    else:
        seriesinfo_in_title = None
        final_title = title

    # for MOST collections where the final word is not needed for the title
    arch_coll_title_regex = r'^(.*)(?:\s+)(\w+)'

    arch_col_split = re.match(arch_coll_title_regex, arch_coll_title)
    collection_suffix = arch_col_split.group(2)
    collection_suffix = ' ' + collection_suffix.lower()

    # series_split = series.split(':')
    if pd.isna(series) or not isinstance(series, str):
        series_suffix = collection_suffix
    else:
        series_split = series.split(':')
        series_suffix = series_split[1]

    # remember to add {{series_split[1]} back if you remove
    if seriesinfo_in_title is not None and series_suffix != '':
        new_title = f"{final_title}, {arch_col_split.group(1)} {seriesinfo_in_title}{series_suffix}, {date}"
        if date is None:
            new_title = f"{final_title}, {arch_col_split.group(1)} {seriesinfo_in_title}{series_suffix}"
    else:
        new_title = f"{final_title}, {arch_coll_title}, {date}"
        if date is not None:
            new_title = f"{final_title}, {arch_col_split.group(1)}{series_suffix}, {date}"
        else:
            new_title = f"{final_title}, {arch_col_split.group(1)}{series_suffix}"

    return new_title

def finalize_callnumber(row):
    manuscript = row['Call Number']
    box = row['Box']
    folder = row['Folder']

    final_callnumber = f"{manuscript} Box {box} Folder {folder}"
    return final_callnumber

def parse_range(folder_range):
    # Parse the range string and return start and end values
    match = re.match(r'(\d+)-(\d+)([a-zA-Z]*)', folder_range)
    if match:
        start, end, end_suffix = match.groups()
        end_value = int(end) if end else int(end)
        return start, str(end_value) + end_suffix
    else:
        return None, None

def return_link(primo_link):
    # Just grab the instance of the url from the content field
    match = re.match(r'^.*?(\d{3,}).*?$', primo_link)
    if match:
        return match.group(1)
    else:
        return None

def is_valid_folder_value(value):
    # Check if the value is not empty and contains only alphanumeric characters
    return value and (value.isalnum() or value.isdigit())

# truncating titles at the first word break after n=150 characters; increase 'length' input parameter to change n
def truncate_title(field, max_length=125):
    if field is None or not isinstance(field, str):
        return None

    if len(field) <= max_length:
        return field
    else:
        truncated_field = field[:max_length - 3]
        return f"{truncated_field}..."

# Assign formats based on series names
def assign_format(row):
    if pd.notna(row['Series Name']):
        if 'correspondence' in row['Series Name']:
            return 'Correspondence'
        elif 'scrapbooks' in row['Series Name']:
            return 'Scrapbooks'
        elif 'photographs' in row['Series Name']:
            return 'Photographs'
        elif 'works' in row['Series Name']:
            return 'Writings (Documents)'
        else:
            return ''
    else:
        return ''

def find_matched_languages(language_text, languages_to_search):
    lang_pattern = '|'.join(rf'\b{re.escape(lang)}\b' for lang in languages_to_search)
    match = re.search(lang_pattern, language_text, flags=re.IGNORECASE)
    return match.group(0) if match else None

languages_to_search = ['English', 'German', 'French', 'Spanish; Castilian', 'Italian', 'Swedish', 'Polish', 'Cherokee', 'Japanese', 'Lithuanian', 'Russian', 'Yiddish', 'Siksika', 'Czech', 'Danish', 'Dutch; Flemish', 'Hebrew', 'Navajo; Navaho', 'Slovak', 'Thai', 'Welsh']

with open('all_archival_obj_info.json', 'r') as new_file:
    all_arch_obj_info = json.load(new_file)

df = pd.json_normalize(all_arch_obj_info)

# Comment back in if you need to see how the JSON flattens
df.to_csv('see_json_normalizec.csv', index=False)

# new_df = pd.DataFrame()
# (columns=['Title_Aspace', 'Archival Collection Title', 'Ref ID', 'Created Date', 'Language', 'Series Name', 'Folder'])

# Grab the beginning of the call number from the resource record 'ead_id'
call_number_start = df.loc[df['level'] == 'collection', 'ead_id'].values[0]

# Grab catalog url & abstract
primo_link = None
abstract = None
collection_row = df[df['level'] == 'collection']

if not collection_row.empty:
    for catalog_record in collection_row['notes'].iloc[0]:
            if isinstance(catalog_record, dict) and catalog_record.get('label') == 'Catalog Record':
                for link in catalog_record.get('subnotes', []):
                    if link.get('jsonmodel_type') == 'note_text':
                        primo_link = link.get('content')
    for abstract in collection_row['notes'].iloc[0]:
            if isinstance(abstract, dict) and abstract.get('label') == 'Abstract':
                abtext = abstract.get('content')
                abtext = ''.join(abtext)

if primo_link is not None:
    catalog_link = return_link(primo_link)

# Grab the date of the entire collection if no date, undated, n.d.
collection_date = None
if (df['level'] == 'collection').any():
    for datelist in df.loc[df['level'] == 'collection', 'dates']:
        for date in datelist:
            collection_date = date.get('expression')

# Create a uri mapping to grab series information from each folder record
uri_mapping = {row['uri']: row for index, row in df.iterrows()}

# print(uri_mapping)

collection_title = []
# bioghist_contents = []
series_name = []
series_note = []
rows_list = []
created_date = None
for index, row in df[(df['level'].isin(['otherlevel', 'file', 'item']))].iterrows():
    matched_languages = []
    title = truncate_title(row['title'])
    ref_id = row['ref_id']

    # Grab the created date from the otherlevel arrays
    date_list = row['dates']

    if isinstance(date_list, list) and len(date_list) > 0:
        # Assuming there's only one date entry in the list, extract the "expression"
        date_entry = date_list[0]
        created_date = date_entry.get('expression')
        
        if created_date is None:
            created_date = collection_date
        elif created_date.lower() in ('n.d.' or 'no date' or 'undated'):
            created_date = collection_date
        elif '[' in created_date:
            created_date = created_date.replace("[", "").replace("]","")
    
    ancestors = row['ancestors']
    if isinstance(ancestors, list):
        for ancestor in ancestors:
            if ancestor['level'] == 'series':
                uri = ancestor['ref']
                # print(uri)
                if uri in uri_mapping:
                    access_uri = uri_mapping.get(uri)
                    if access_uri.any():
                        series_name = access_uri['title']
                        # print(series_name)
    
    resource_uri = row['resource.ref']
    if resource_uri in uri_mapping:
        resource = uri_mapping.get(resource_uri)
        if resource.any():
            collection_title = resource['title']
            
            # print(collection_title)

            # if 'notes' in resource and isinstance(resource['notes'], list):
            #     for notes in resource['notes']:
            #         if notes.get('type') == 'bioghist':
            #             for subnote in notes.get('subnotes', []):
            #                 if subnote.get('jsonmodel_type') == 'note_text':
            #                     content = subnote.get('content')
            #                     if content:
            #                         soup = BeautifulSoup(content, 'html.parser')
            #                         bioghist_contents = soup.get_text()
            #                         break

            for lang_material in resource.get('lang_materials', []):
                if isinstance(lang_material, dict) and lang_material.get('jsonmodel_type') == 'lang_material':
                    for lang_note in lang_material.get('notes', []):
                        if lang_note.get('jsonmodel_type') == 'note_langmaterial':
                            language_text_list = lang_note.get('content')
                            for language_text in language_text_list:
                                matched_languages = find_matched_languages(language_text, languages_to_search)
    
    instances = row['instances']
    if isinstance(instances, list):
        for instance in instances:
            if 'sub_container' in instance:
                sub_container = instance['sub_container']
                folder_number_range = sub_container.get('indicator_2')

                new_row = []
                folder_numbers = None
                if folder_number_range is not None:
                    if '-' in folder_number_range:
                        # start, end = folder_number_range.split('-')
                        start, end = parse_range(folder_number_range)
                        if start is not None and end is not None:
                            if end.isdigit():
                                for folder_value in range(int(start), int(end) + 1):
                                    folder_str = str(folder_value)
                                    if is_valid_folder_value(folder_str):
                                        new_row = {
                                                'Title_Aspace': title,
                                                'Ref ID': ref_id,
                                                'Created Date': created_date,
                                                'Folder': str(folder_value),
                                                'Series Name': series_name,
                                                'Archival Collection Title': collection_title,
                                                'Language': matched_languages
                                                }
                                        rows_list.append(new_row)
                    else:
                        new_row = {
                                'Title_Aspace': title,
                                'Ref ID': ref_id,
                                'Created Date': created_date,
                                'Folder': str(folder_number_range),
                                'Series Name': series_name,
                                'Archival Collection Title': collection_title,
                                'Language': matched_languages
                            }
                        rows_list.append(new_row)

    # new_df = pd.concat([new_df, pd.DataFrame({'Title_Aspace': [title], 'Ref ID': [ref_id], 'Created Date': [created_date], 'Language': [matched_languages], 'Folder': [folder_numbers]})], ignore_index=True)

# Grab the Scope and Content note from the resource record 'notes'
# summary = None
# for notes_list in df['notes']:
#     for notes in notes_list:
#         if notes.get('type') == 'scopecontent':
#             for subnote in notes.get('subnotes', []):
#                 if subnote.get('jsonmodel_type') == 'note_text':
#                     summary = subnote.get('content')
#                     break
#     if summary:
#         break

# if summary:
#     soup = BeautifulSoup(summary, 'html.parser')
#     summary = soup.get_text()

new_df = pd.DataFrame(rows_list)

# Grab the ArchivesSpace resource URL from the resource record 'uri'
finding_aid = df.loc[df['level'] == 'collection', 'uri'].values[0]

# Creating columns in dataframe
new_df['Call Number'] = call_number_start
# new_df['Archival Collection Title] = collection_title'
# new_df['Biographical/Historical Note'] = bioghist_contents
# new_df['Summary Long'] = summary
# new_df['Language'] = matched_languages
# new_df['Series Name'] = series_name
# new_df['Series Content'] = series_note
new_df['Description'] = f'{abtext}'
new_df['Series Name'] = new_df['Series Name'].str.lower()
new_df['Finding Aid Link'] = f"<a href='https://archives.newberry.org{finding_aid}' target='_blank'>View finding aid</a> | <a href='https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma{catalog_link}' target='_blank'>View record</a>"
new_df['Open Access Policy'] = "The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to <a href='https://www.newberry.org/policies#open-access' target='_blank'>these terms and conditions.</a>"
new_df['Help'] = "Need help finding, searching, sharing, or downloading? Check out our <a href='https://digital.newberry.org/help/' target='_blank'>help page</a>!"
new_df['Contributing Institution'] = 'Newberry Library'

new_df['Format'] = new_df.apply(assign_format, axis=1)

new_df.to_csv('json_to_csv.csv', index=False)

csv_file_path = args.Cortex_CSV

cortex_df = pd.read_csv(csv_file_path)

# Extract the folder number from the file name. Look at filename to match how folder is indicated, can be fl, fol, f.
folder_number_cortex = r'f[ol]l?_0*(\d+[a-z]*)_'
cortex_df['Folder'] = cortex_df['Original file name'].str.extract(folder_number_cortex).astype(str)

# Extract the bibid from the file name
bibid = r'^(\d+)_'
cortex_df['BibID'] = cortex_df['Original file name'].str.extract(bibid).astype(str)

# Extract the box number from the file name. Look at filename to match how box is indicated, can be bx, box, b.
# box_number = r'bx_0+(\d+)'
box_number = r'b[o]?x_0*(\d+)'
cortex_df['Box'] = cortex_df['Original file name'].str.extract(box_number).astype(str)
# print(cortex_df['Box'])

cortex_df.to_csv('testing_issues.csv', index=False)

merged_df = cortex_df.merge(new_df, on='Folder', how='inner')

# Save and open the merged dataframe if you think there may be issues before finalizing the columns.
# merged_df.to_csv('test_to_see_issues.csv', index=False)

merged_df['Title_Aspace'] = merged_df.apply(process_titles, axis=1)
merged_df['Call Number'] = merged_df.apply(finalize_callnumber, axis=1)

merged_df['Title'] = merged_df['Title_Aspace']

final_df_columns = ['Unique identifier', 'BibID', 'Original file name', 'Title', 'Created Date', 'Language', 'Description', 'Format', 'Contributing Institution', 'Archival Collection Title', 'Finding Aid Link', 'Call Number', 'Open Access Policy', 'Ref ID', 'Help']

final_df = merged_df[final_df_columns]

final_df.to_csv('aspace_to_cortex_csv.csv', encoding='utf-8-sig', index=False)