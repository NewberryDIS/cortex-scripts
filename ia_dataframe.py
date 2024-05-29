import csv
from pprint import pprint as pp
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='csv of ia metadata')
args = parser.parse_args()


def replace_commas_with_pipes(string):
	if ',' in string:
		string = string.split(',')
		string = '|'.join(string)
	return string


def create_data_dict(row):
	d = {}
	d['TITLE'] = row['title']
	# d['DESCRIPTION'] = row['description']
	d['DATE_DISPLAY'] = row['date']
	# d['FILENAME'] = row['identifier']+'.jp2'
	# d['DATE_SORT'] = row['Sort Date']
	# d['PLACE'] = replace_commas_with_pipes(row['coverage'])
	# d['CREATOR'] = row['creator']
	# d['PUBLISHER_ORIGINAL'] = replace_commas_with_pipes(row['Publisher'])
	d['SUBJECTS'] = replace_commas_with_pipes(row['subject']) # Format this
	d['CONTRIBUTING_INSTITUTION'] = row['contributor']
	d['FORMAT'] = replace_commas_with_pipes(row['format']) # Format this
	# d['DCMITYPE'] = row['type']
	d['DESCRIPTION'] = row['description']
	d['CALL_NUMBER'] = row['call_number']
	d['LANGUAGE'] = 'English'
	# d['ARCHIVAL_COLLECTION'] = row['Archival Collection Title']
	# d['CATALOG_LINK'] = row['Catalog Record / Collection Guide']
	# d['BIOGRAPHICAL/HISTORICAL NOTE'] = row['Biographical/Historical Note Long']
	# d['SUMMARY'] = 
	# d['OA_POLICY'] = "The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to <a href='https://www.newberry.org/policies' target='_blank'>these terms and conditions.</a>"
	# d['BIBID'] = row['BibID Link']
	# d['Parent Folder Unique Identifier'] = row['Parent Folder Unique Identifier']
	# d['SubType name'] = row['Sub type ID']
	return d


rows = []
titles = []
count = 0
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		# pp(row.keys())
		d = create_data_dict(row)
		if row['format'] == 'Postcards,Archive BitTorrent,DjVuTXT,Djvu XML,Generic Raw Book Zip,Item Tile,Metadata,OCR Page Index,OCR Search Text,Page Numbers JSON,Scandata,Single Page Processed JP2 ZIP,Text PDF,chOCR,hOCR':
			d['FORMAT'] = 'Postcards'
		# if row['description'] == '6.5 x 8.5 negative. From a collection including images showing city street views, buildings, businesses, homes, churches, parks, family, and friends and are primarily of Chicago and Grand Rapids, Michigan. Also includes images taken in other locations in Illinois, Michigan, Missouri, and Iowa. Michaelis often wrote photograph information on the negative sleeves, including the time of day, weather conditions, and the stop used. This information has been transcribed on the enclosures for each negative. Because the negatives are in original order by size, related images are not always grouped together and are not chronological.':
		# 	d['FORMAT_EXTENT'] = '6.5 x 8.5 negative'
		# if row['description'] == '5 x 7 negative. From a collection including images showing city street views, buildings, businesses, homes, churches, parks, family, and friends and are primarily of Chicago and Grand Rapids, Michigan. Also includes images taken in other locations in Illinois, Michigan, Missouri, and Iowa. Michaelis often wrote photograph information on the negative sleeves, including the time of day, weather conditions, and the stop used. This information has been transcribed on the enclosures for each negative. Because the negatives are in original order by size, related images are not always grouped together and are not chronological.':
		# 	d['FORMAT_EXTENT'] = '5 x 7 negative'
		# if row['format'] == 'Photographs; Glass plate negatives,Archive BitTorrent,JPEG,JPEG Thumb,Metadata':
		# 	d['FORMAT'] = 'Photographs|Glass plate negatives'
		if row['contributor'] == 'The Newberry Library':
			d['CONTRIBUTING_INSTITUTION'] = 'Newberry Library'
		rows.append(d)


keys = rows[0].keys()
with open('batch_ia_metadata.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)