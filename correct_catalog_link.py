from pprint import pprint as pp
import argparse
import csv
import re
import os




if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='')
	parser.add_argument('csv', help='csv of AV data')
	parser.add_argument('csv2', help='csv of A or V data from Cortex')
	args = parser.parse_args()



	# 147981


	rows = []
	with open(args.csv, encoding='utf-8', errors='ignore') as csvf:
		reader = csv.DictReader(csvf)
		for row in reader:
			if row['CATALOG_LINK'] != "":
				regex = r"RecID=([0-9]+)"
				search = re.findall(regex, row['CATALOG_LINK'])
				if len(search) != 0:
					bibid = search[0]
					correct_link = f'https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma99{bibid}8805867'
					row['CATALOG_LINK'] = correct_link
			rows.append(row)



	keys = rows[0].keys()
	with open(args.csv2, 'w', newline='', encoding='utf-8', errors='ignore') as outfile:
		dict_writer = csv.DictWriter(outfile, keys)
		dict_writer.writeheader()
		dict_writer.writerows(rows)
