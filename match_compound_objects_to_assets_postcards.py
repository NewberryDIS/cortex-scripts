import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re


s = 'Bill Lende collection of tall tale postcards, 1906-2006 [Lende_000367]'
m = re.search(r"\[(\w+)\]", s)
stem = m.group(1)


parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all assets to be moved into virtual compound object folders')
parser.add_argument('csv2', nargs='?', help='CSV of all compound object folders and unique ids for matching')
args = parser.parse_args()


compound_objects = {}
with open(args.csv2, encoding='utf-8', errors='ignore') as compound_objs:
	reader = csv.DictReader(compound_objs)
	for row in reader:
		# pp(row['Title'])
		# pp(row.keys())
		m = re.search(r"\[(\w+)\]", row['Title'])
		if m != None:
			stem = m.group(1)
			compound_objects[stem] = row['\ufeff"Unique Identifier"']

# pp(compound_objects)

rows = []
with open(args.csv1, encoding='utf=8', errors='ignore') as assets_to_be_moved:
	reader = csv.DictReader(assets_to_be_moved)
	for row in reader:
		# pp(row.keys())
		row['Unique identifier'] = row['\ufeff"Unique Identifier"']
		row['Compound Object Unique identifier'] = ''
		for k, v in compound_objects.items():
			if k in row['Original File Name']:
				row['Compound Object Unique identifier'] = v
		# compound_object_id = compound_objects.get(row['Title'])
		# if compound_object_id != None:
		# 	row['Compound Object Unique identifier'] = compound_object_id
			# pp(row)
		rows.append(row)


# pp(rows)
df = pd.DataFrame.from_dict(rows)
df.sort_values(["Original File Name"], 
                    axis=0,
                    ascending=[True], 
                    inplace=True)

df.to_csv(r'assets_to_be_moved.csv', index = False, header=True)
