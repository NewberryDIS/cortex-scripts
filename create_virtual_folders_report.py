import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re



parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of all virtual folders and assets inside')
parser.add_argument('csv2', nargs='?', help='CSV of all assets')
args = parser.parse_args()



d = {}
unique_virtual_folders = {}
with open(args.csv1, encoding='utf-8', newline='', errors='ignore') as csv1_:
	reader = csv.DictReader(csv1_)
	for row in reader:
		if row['Child original filename'] not in d.keys():
			d[row['Child original filename']] = row
		if row['Virtual folder title'] not in unique_virtual_folders.keys():
			data = {}
			# data['Visibility class'] = ''
			data['Virtual folder title'] = row['Virtual folder title']
			unique_virtual_folders[row['Virtual folder title']] = data 



with open(args.csv2, encoding='utf-8', newline='', errors='ignore') as csv2_:
	reader = csv.DictReader(csv2_)
	for data in reader:
		if d.get(data['Original file name']) != None:
			child = d.get(data['Original file name'])
			child['Visibility'] = data['Visibility class']
		if unique_virtual_folders.get(data['Title']) != None:
			if 'compound object' in data['Sub type'].lower():
				compound_object = unique_virtual_folders.get(data['Title'])
				compound_object['Visibility'] = data['Visibility class']
				compound_object['Compound object type'] = data['Sub type']



rows = []
for k, v in d.items():
	v['Compound object title'] = ''
	v['Compound object type'] = ''
	v['Compound object visibility'] = ''
	# pp(v)
	get_co = unique_virtual_folders.get(v['Virtual folder title'])
	if get_co != None:
		# pp(get_co)
		# pp(v)
		try:
			v['Compound object title'] = get_co['Virtual folder title']
			v['Compound object type'] = get_co['Compound object type']
			v['Compound object visibility'] = get_co['Visibility']
			rows.append(v)
		except KeyError:
			continue


pp(len(rows))

dataframe = pd.DataFrame(rows) 
dataframe = dataframe.sort_values(by=['Child original filename'])
dataframe.to_csv('compound_objects_and_assets.csv', index=False, header=True)
