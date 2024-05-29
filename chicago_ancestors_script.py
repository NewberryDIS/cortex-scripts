import csv
from pprint import pprint as pp
import argparse
import re
import html
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of Chicago Ancestors metadata')
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

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&.{4};')
    cleantext = re.sub(cleanr, '', str(raw_html))
#     replacing the special characters
#     cleanr = re.compile ('\\n')
#     cleantext = re.sub(cleanr, ' ', cleantext)
    clean = re.sub('\s+',' ',cleantext)
    return html.unescape(clean) # replaces the special characters

def create_data_dict(row):
	d = {}
	d['TITLE'] = cleanhtml(row['Title'])
	d['ADDRESS 1'] = row['Street Address - Thoroughfare (i.e. Street address)']
	d['ADDRESS 2'] = row['Street Address - Premise (i.e. Apartment / Suite number)']
	d['CITY'] = row['Street Address - Locality (i.e. City)']
	d['STATE'] = row['Street Address - Administrative area (i.e. State / Province)']
	d['COUNTRY'] = row['Street Address - Country']
	d['DENOMINATION'] = cleanhtml(row['Denomination'])
	d['ETHNICITY'] = cleanhtml(row['Ethnicity'])
	d['STRUCTURE_TYPE'] = cleanhtml(row['Structure Type'])
	d['TOPIC'] = cleanhtml(row['Topic'])
	d['DATE_DISPLAY'] = row['Start Year'] + ' to ' + row['End Year']
	d['DATE_SORT'] = row['Start Year'] +'-01-01' + '/' + row['End Year'] + '-01-01'
	d['LATITUDE'] = row['geoplace']
	d['LONGITUDE'] = row['geoplace']
	d['DESCRIPTION'] = row['Body']
	d['USERNAME'] = row['Author uid'] #need to grab just the username from html
	d['SUBMISSION_DATE'] = row['Post date'] #change to YYYY-MM-DD format
	# d['COMMENT'] = row['Newberry Open Access Policy']
	# d['COMMENTER_NAME'] = row['Rights Status']
	# d['COMMENTER_SUBJECT'] = row['Call Number']
	return d

rows = []
titles = []
count = 0
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		d = create_data_dict(row)
        # latitude = row['geoplace'].split('_')[1]
        # if row
		# if d['BIBID'] != '' and len(d['TITLE']) < 186:
		# 	d['TITLE'] = f'{d["TITLE"]} [{d["BIBID"]}]'
		# if row['\ufeff"SubType name"'] == 'Text':
		# 	d['Sub type ID'] = 'DO_NL1ND000000013993'
		# if row['\ufeff"SubType name"'] == 'Image':
		# 	d['Sub type ID'] = 'DO_NL1ND000000013799'
		rows.append(d)


keys = rows[0].keys()
with open('ca_metadata.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)