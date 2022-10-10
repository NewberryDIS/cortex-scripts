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


def create_data_dict(row):
	d = {}
	d['FILENAME'] = row['Original File Name']
	d['TITLE'] = row['Title']
	d['DESCRIPTION'] = row['Description / Data']
	d['DATE_DISPLAY'] = row['Date Created']
	d['DATE_SORT'] = row['Sort Date']
	d['PLACE'] = replace_commas_with_pipes(row['Place'])
	d['CREATOR'] = replace_commas_with_pipes(row['Source / Creator'])
	d['PUBLISHER_ORIGINAL'] = replace_commas_with_pipes(row['Publisher'])
	d['SUBJECTS'] = replace_commas_with_pipes(row['Subject']) # Format this
	d['CONTRIBUTING_INSTITUTION'] = row['Contributing Institution']
	d['FORMAT'] = replace_commas_with_pipes(row['Format']) # Format this
	d['DCMITYPE'] = row['Dcmi Type']
	d['FORMAT_EXTENT'] = row['Extent']
	d['LANGUAGE'] = replace_commas_with_pipes(row['Language']) # Format this
	d['ARCHIVAL_COLLECTION'] = row['Archival Collection Title']
	d['CATALOG_LINK'] = row['Catalog Record / Collection Guide']
	d['BIOGRAPHICAL/HISTORICAL NOTE'] = row['Biographical/Historical Note Long']
	d['SUMMARY'] = row['Summary Long']
	d['OA_POLICY'] = row['Newberry Open Access Policy']
	d['STANDARDIZED_RIGHTS'] = row['Rights Status']
	d['CALL_NUMBER'] = row['Call Number']
	d['BIBID'] = row['Bibid Link']
	d['Parent Folder Unique Identifier'] = row['Parent Folder Unique Identifier']
	return d


rows = []
titles = []
count = 0
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_file:
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
			rows.append(d)


keys = rows[0].keys()
with open('lead_objects_with_metadata.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)

