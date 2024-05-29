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
		if row['Is Lead'] == 'True':
			identifier1 = row['Original File Name'].split('_')[1]
			identifier2 = row['Original File Name'].split('_')[2]
			row['Title'] = f'{row["Title"]} [{identifier1} {identifier2}]'
			pp(row['Title'])
			rows.append(row)



# pp(rows)
# pp(len(rows))

keys = rows[0].keys()
with open('japanese_lead_objects.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)



# df = pd.DataFrame.from_dict(rows)
# df.to_csv(r'lead_objects.csv', index = False, header=True)