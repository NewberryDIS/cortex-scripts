import csv
from pprint import pprint as pp
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all assets to be made into compound objects')
args = parser.parse_args()


def replace_commas_with_pipes(string):
	if ',' in string:
		string = string.split(',')
		string = '|'.join(string)
	return string

def replace_to_with_backslash(string):
	if ' to ' in string:
		string = string.split(' to ')
		string = '/'.join(string)
	return string


def create_data_dict(row):
	d = {}
	d['FILENAME'] = row['Original file name']
	d['TITLE'] = row['Title']
	d['DESCRIPTION'] = row['Description']
	d['DATE_DISPLAY'] = row['Date Created']
	d['DATE_SORT'] = replace_to_with_backslash(row['Sort Date'])
	d['PLACE'] = row['Place']
	d['CREATOR'] = row['Creator']
	d['PUBLISHER_ORIGINAL'] = row['Publisher']
	d['SUBJECTS'] = row['Subject'] # Format this
	d['CONTRIBUTING_INSTITUTION'] = row['Contributing Institution']
	d['FORMAT'] = row['Format'] # Format this
	d['DCMITYPE'] = row['DCMI Type']
	d['FORMAT_EXTENT'] = row['Extent']
	d['LANGUAGE'] = row['Language'] # Format this
	d['ARCHIVAL_COLLECTION'] = row['Archival Collection Title']
	d['CATALOG_LINK'] = row['Catalog Record / Collection Guide']
	d['BIOGRAPHICAL/HISTORICAL NOTE'] = row['Biographical/Historical Note Long']
	d['SUMMARY'] = row['Summary Long']
	d['OA_POLICY'] = row['Newberry Open Access Policy']
	d['STANDARDIZED_RIGHTS'] = row['Rights Status']
	d['CALL_NUMBER'] = row['Call Number']
	d['BIBID'] = row['BibID']
	d['Parent Folder Unique Identifier'] = row['Parent Folder Unique Identifier']
	d['Sub type ID'] = row['SubType name']
	return d

rows = []
titles = []
count = 0
with open(args.csv1, encoding='utf-8-sig', errors='ignore') as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		# pp(row.keys())
		# pp(row['Is Lead'])
		if row['Is Lead'] == 'True':
			# count += 1
			# pp(count)
			d = create_data_dict(row)
			if d['BIBID'] != '' and len(d['TITLE']) < 186:
				d['TITLE'] = f'{d["TITLE"]} [{d["BIBID"]}]'
			# identifier1 = row['Original file name'].split('_')[1]
			# identifier2 = row['Original file name'].split('_')[2]
			# identifier3 = row['Original file name'].split('_')[4]
			# identifier4 = row['Original file name'].split('_')[5]
			# d['TITLE'] = f'{row["Title"]} [{identifier1} {identifier2}]'
			# d['TITLE'] = f'{row["Title"]} [{identifier1}_{identifier3}]'
			if row['SubType name'] == 'Text':
				d['Sub type ID'] = 'DO_NL1ND000000013993'
			if row['SubType name'] == 'Image':
				d['Sub type ID'] = 'DO_NL1ND000000013799'
			if row ['SubType name'] == 'Still Image':
				d['Sub type ID'] = 'DO_NL1ND000000013799'
			rows.append(d)


keys = rows[0].keys()
with open('lead_objects_with_metadata_titlediff.csv', 'w', encoding='utf-8-sig', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)