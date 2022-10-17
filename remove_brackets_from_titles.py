import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re




parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of assets')
args = parser.parse_args()



# s = 'I Am [45161] Person [3021521]'
# r = re.findall(r'(\[[\w]*\]$)', s)
# pp(r)


rows = []
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_:
	reader = csv.DictReader(csv_)
	for row in reader:
		# pp(row.keys())
		if 'box' not in row['\ufeff"Title"']:
			if '[' in row['\ufeff"Title"']:
				r = re.search(r'(\[[\w]*\]$)', row['\ufeff"Title"'])
				if r != None:
					row['Title'] = row['\ufeff"Title"'].replace(r.group(), '').strip()
					pp(row['Title'])
					rows.append(row)



pd.DataFrame(rows).to_csv('out.csv', index=False, header=True)


