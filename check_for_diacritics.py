import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re

parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all assets to be made into compound objects')
args = parser.parse_args()


BAD_CHARS = '©Ã§¬Œ¶¼¡Ì€ˆ' # Add more diacritic characters here that you want to check for


def check_if_diacritics_in_field(field):
	diacritic_count = 0
	for char in BAD_CHARS:
		if char in field:
			diacritic_count	+= 1

	return diacritic_count	


rows = []
count = 0
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_:
	reader = csv.DictReader(csv_)
	for row in reader:
		# pp(row.keys())
		if check_if_diacritics_in_field(row['Extent']) >= 1: # Or any other field you wish to check for in place of row['Title']
			# count += 1
			# pp(count)
			# pp(row['Title'])
			rows.append(row)


pp(f'How many assets with diacritic issues: {len(rows)}')


df = pd.DataFrame(rows)
df.to_csv('assets_with_diacritics.csv', index=False, header=True)


