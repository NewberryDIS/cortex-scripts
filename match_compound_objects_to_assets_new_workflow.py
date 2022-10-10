import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re


# s = 'Index to the Journal of the proceedings of the City Council of the City of Chicago [proceedingsofcit139chic]'
# m = re.search(r"\[(\w+)\]", s)
# stem = m.group(1)
# pp(stem)

parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all assets to be moved into virtual compound object folders')
parser.add_argument('csv2', nargs='?', help='CSV of all compound object folders and unique ids for matching')
args = parser.parse_args()


compound_objects = {}
with open(args.csv2, encoding='utf-8', errors='ignore') as compound_objs:
	reader = csv.DictReader(compound_objs)
	for row in reader:
		compound_objects[row['Title']] = row['\ufeff"Unique Identifier"']

pp(compound_objects)

rows = []
with open(args.csv1, encoding='utf-8', errors='ignore') as assets_to_be_moved:
	reader = csv.DictReader(assets_to_be_moved)
	for row in reader:
# 		pp(row.keys())
		row['Unique identifier'] = row['\ufeff"Unique Identifier"']
		get_id = compound_objects.get(row['Title'])
		if get_id != None:
			row['Compound Object Unique identifier'] = get_id
			pp(row['Compound Object Unique identifier'])
			rows.append(row)

pp(len(rows))
# pp(rows)

df = pd.DataFrame.from_dict(rows)
df.sort_values(["Original File Name"], 
                    axis=0,
                    ascending=[True], 
                    inplace=True)

df.to_csv(r'new_assets_to_be_moved.csv', index = False, header=True)

