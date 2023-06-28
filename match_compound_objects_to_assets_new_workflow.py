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
with open(args.csv2, encoding='utf-8-sig', errors='ignore') as compound_objs:
	reader = csv.DictReader(compound_objs)
	for row in reader:
		# pp(row.keys())
		compound_objects[row['Title']] = row['Unique identifier']

pp(compound_objects)

rows = []
with open(args.csv1, encoding='utf-8-sig', errors='ignore') as assets_to_be_moved:
	reader = csv.DictReader(assets_to_be_moved)
	for row in reader:
		pp(row['Title'])
		row['Unique identifier'] = row['Unique identifier']
		# identifier1 = row['Original file name'].split('_')[5]
		# identifier2 = row['Original file name'].split('_')[8]
		# identifier3 = row['Original file name'].split('_')[4]
		# identifier4 = row['Original file name'].split('_')[5]
		# row['Title'] = f'{row["Title"]} [{identifier1}]'
		row['Title'] = f'{row["Title"]} [{row["BibID"]}]'
		get_id = compound_objects.get(row['Title'])
		pp(row['Title'])
		pp(get_id)
		if get_id != None:
			row['Compound Object Unique identifier'] = get_id
			pp(row['Compound Object Unique identifier'])
			rows.append(row)

pp(len(rows))
# pp(rows)

# try:
# 	keys = rows[0].keys()
# 	with open('assets_to_be_moved.csv', 'w', newline='', errors='ignore', encoding='utf-8')  as output_file:
# 			dict_writer = csv.DictWriter(output_file, keys)
# 			dict_writer.writeheader()
# 			dict_writer.writerows(rows)
# except IndexError:
# 	pp("rows empty")
df = pd.DataFrame.from_dict(rows)
# pp(row.keys())
df.sort_values(['Original file name'], 
                    axis=0,
                    ascending=[True], 
                    inplace=True)

df.to_csv(r'new_assets_to_be_moved.csv', index = False, header=True)

