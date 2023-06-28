import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re




parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of assets')
args = parser.parse_args()



# s = 'I Am Person [box 000012]'
# r = re.search(r'(\[[0-9]*\]$)', s)
# pp(r.group())
 

rows = []
with open(args.csv1, encoding='utf-8', errors='ignore') as csv_:
    reader = csv.DictReader(csv_)
    for row in reader:
        # pp(row.keys())
        if '[' in row['\ufeff"Title"']:
            r = re.search(r'(\[[0-9]*\]$)', row['\ufeff"Title"'])
            pp(row['\ufeff"Title"'])
            if r != None:
                # if 'box' in r.group() and 'vol' in r.group():
                row['\ufeff"Title"'] = row['\ufeff"Title"'].replace(r.group(), '').strip()
                pp(row['\ufeff"Title"'])
                rows.append(row)
 

keys = rows[0].keys()
with open('removedbrackets.csv', 'w', encoding='utf-8', newline="", errors='ignore') as outfile:
  writer = csv.DictWriter(outfile, keys)
  writer.writeheader()
  writer.writerows(rows)