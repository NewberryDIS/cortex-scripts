import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re

parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all assets to be made into compound objects')
args = parser.parse_args()


# t = 'dog,cat,fish'
# d = 'John Smith, 1899'

# r = re.search(r'([a-zA-Z0-9]*,[a-zA-Z0-9])', t)
# # pp(r.group())

rows = []
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_:
	reader = csv.DictReader(csv_)
	for row in reader:
		# pp(row.keys())
		if ',' in row['Level0_Label']:
			r = re.search(r'([a-zA-Z0-9]*,[a-zA-Z0-9]*)', row['Level0_Label'])
			if r != None:
				# pp(row['Level0_Label'])
				row['Delete_Y_N'] = 'Y'
				rows.append(row)


pp(len(rows))

keys = rows[0].keys()
with open('tags_to_delete.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)