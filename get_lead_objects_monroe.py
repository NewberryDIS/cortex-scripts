import csv
from pprint import pprint as pp
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all assets to be made into compound objects')
args = parser.parse_args()


rows = []
titles = []
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		# pp(row['Is Lead'])
		if row['Is Lead'] == 'TRUE':
			if 'sports' in row['Title'].lower():
				identifier = row['Original file name'].split('_')[2]
				row['Title'] = f'{row["Title"]} [{identifier}]'
				# pp(row['Title'])
			if 'exposition' in row['Title'].lower():
				identifier = row['Original file name'].split('_')[6]
				row['Title'] = f'{row["Title"]} [{identifier}]'
			rows.append(row)



pp(rows)
pp(len(rows))

keys = rows[0].keys()
with open('monroe_lead_objects.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)



# df = pd.DataFrame.from_dict(rows)
# df.to_csv(r'lead_objects.csv', index = False, header=True)