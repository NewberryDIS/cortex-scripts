import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re


# s = 'James R. Powell Route 66 postcard collection, 1926-1960s [000244 01]'
# m = re.search(r"\[(\w+\s\w+)\]", s)
# stem = m.group(1)
# stem = stem.split(' ')
# stem = "_".join(stem)
# pp(stem)

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
		m = re.search(r"\[(\w+\s\w+)\]", row['Title'])
		if m != None:
			stem = m.group(1)
			stem = stem.split(' ')
			stem = "_".join(stem)
			compound_objects[stem] = row['\ufeffUnique Identifier']

# pp(compound_objects)

rows = []
with open(args.csv1, encoding='utf=8', errors='ignore') as assets_to_be_moved:
	reader = csv.DictReader(assets_to_be_moved)
	for row in reader:
		# pp(row.keys())
		row['Unique identifier'] = row['Unique identifier']
		row['Compound Object Unique identifier'] = ''
		for k, v in compound_objects.items():
			if k in row['Original file name']:
				row['Compound Object Unique identifier'] = v
		identifier1 = row['Original file name'].split('_')[7]
		identifier2 = row['Original file name'].split('_')[8]
		compound_object_id = compound_objects.get(row['Title'] + identifier1 + identifier2)
		# pp(compound_object_id)
		# if compound_object_id != None:
		# 	row['Compound Object Unique identifier'] = compound_object_id
		# 	pp(row)
		rows.append(row)


# pp(rows)
df = pd.DataFrame.from_dict(rows)
df.sort_values(["Original file name"], 
                    axis=0,
                    ascending=[True], 
                    inplace=True)

df.to_csv(r'assets_to_be_moved.csv', index = False, header=True)

