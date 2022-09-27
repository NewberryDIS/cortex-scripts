import csv
from pprint import pprint as pp
import argparse
import pandas as pd



parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all assets to be moved into virtual compound object folders')
parser.add_argument('csv2', nargs='?', help='CSV of all compound object folders and unique ids for matching')
args = parser.parse_args()


compound_objects = {}
with open(args.csv2, encoding='utf-8', errors='ignore') as compound_objs:
	reader = csv.DictReader(compound_objs)
	for row in reader:
		# pp(row.keys())
		compound_objects[row['Title']] = row['\ufeff"Unique Identifier"']


count = 0
rows = []
with open(args.csv1, encoding='utf=8', errors='ignore') as assets_to_be_moved:
	reader = csv.DictReader(assets_to_be_moved)
	for row in reader:
		pp(row.keys())
		row['Unique identifier'] = row['\ufeff"Unique identifier"']
		row['Compound Object Unique identifier'] = ''
		compound_object_id = compound_objects.get(row['Title'])
		if compound_object_id != None:
			count += 1
			pp(count)
			pp(compound_object_id)
			row['Compound Object Unique identifier'] = compound_object_id
			pp(row['Compound Object Unique identifier'])
			# pp(row)
			# rows.append(row)
		if row['Compound Object Unique identifier'] != '':
			rows.append(row)


# pp(len(rows))

keys = rows[0].keys()
with open('assets_to_be_moved.csv', 'w', encoding='utf-8', newline="", errors='ignore') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)

# df = pd.DataFrame.from_dict(rows)
# df.sort_values(["Original file name"], 
#                     axis=0,
#                     ascending=[True], 
#                     inplace=True)

# df.to_csv(r'assets_to_be_moved.csv', index = False, header=True)

