from pprint import pprint as pp
import argparse
import csv
import re
import os




if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='')
	parser.add_argument('csv', help='csv of alma data')
	# parser.add_argument('outfile', help='csv of alma data')
	args = parser.parse_args()


	bibids = {}
	with open(args.csv, encoding='utf-8', errors='ignore') as csv_file:
		reader = csv.DictReader(csv_file)
		for row in reader:
			if row['BIBID'] not in bibids.keys():
				bibids[row['BIBID']] = []
				bibids[row['BIBID']].append(row)
			else:
				bibids[row['BIBID']].append(row)


	os.chdir('metadata')
	for bibid, rows in bibids.items():
		stem = rows[0]['FILENAME'][:20]
		filename = f'Central_{stem}_{bibid}.csv'
		keys = rows[0].keys()
		with open(filename, 'w', newline='', encoding='utf-8', errors='ignore') as outfile:
			dict_writer = csv.DictWriter(outfile, keys)
			dict_writer.writeheader()
			dict_writer.writerows(rows)