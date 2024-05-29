import urllib.request
import json, csv, re, os, sys
import xml.etree.ElementTree as ET
from datetime import date
import requests
import config
from pprint import pprint as pp
import time
import argparse
import almaFunctions as af

start = time.time()

curYear = date.today().year
today = str(date.today())

# redact api key before pushing
apikey = config.apiKey

reviewSet = []


# # # originally recordlist was made to confirm bibids were present and find them if absent - this can probably be refactored but I don't think it makes much difference
recordList = []

parser = argparse.ArgumentParser()
parser.add_argument('Cortex_folders', nargs='*', default=['NL1N1GC', 'NL1N3WF', 'NL1N3W9', 'NL1N909'], help='Unique identifier of folder wish to add metadata to assets for')
args = parser.parse_args()
folders = args.Cortex_folders
pp(folders)


# Run through stacking rule folders in Cortex and pull recent ingests
authenticate_url = f'https://collections.newberry.org/API/Authentication/v1.0/Login?Login={config.username}&Password={config.password}&format=json'
authenticate = requests.get(authenticate_url)

token = authenticate.json()
token = token['APIResponse']['Token']
token = f'&token={token}'
json_suffix = '&format=json'
pp('Authenticated!')

# NL19QTJ NL19QA4 NL19PQJ NL19I08 NL19Q1E NL1XCEQ NL19Q8Z NL19QCQ NL19Q4I NL1XCEQ

for folder in folders:
	url = f'https://collections.newberry.org/API/search/v3.0/search?query=OriginalSubmissionNumber:{folder}&fields=SystemIdentifier,Title,OriginalFilename,ParentFolderTitle,CoreField.Purpose{token}{json_suffix}'
	get_folder = requests.get(url)
	folder_response = get_folder.json()
	total = folder_response['APIResponse']['GlobalInfo']['TotalCount']
	pp(total)
	items = folder_response['APIResponse']['Items']
	# pp(items)
	for item in items:
		if item['CoreField.Purpose'] == 'Public' or item['CoreField.Purpose'] == 'Pending process':
			if item['OriginalFilename'][:4].isdigit() != True:
				d = {}
				d['FILENAME'] = item['OriginalFilename']
				d['BIBID'] = ''
				# pp(f'Getting data for: {item["OriginalFilename"]}')
				# bibid_dict = af.get_bibid_dict(item['OriginalFilename'])
				recordList.append(d)
	nextPage = folder_response['APIResponse']['GlobalInfo'].get('NextPage')
	while nextPage != None:
		get_folder = requests.get(f'{nextPage["href"]}{json_suffix}')
		folder_response = get_folder.json()
		for item in folder_response['APIResponse']['Items']:
			if item['CoreField.Purpose'] == 'Public' or item['CoreField.Purpose'] == 'Pending process':
				if item['OriginalFilename'][:4].isdigit() != True:
					d = {}
					d['FILENAME'] = item['OriginalFilename']
					d['BIBID'] = ''
					# pp(f'Getting data for: {item["OriginalFilename"]}')
					# bibid_dict = af.get_bibid_dict(item['OriginalFilename'])
					recordList.append(d)
		nextPage = folder_response['APIResponse']['GlobalInfo'].get('NextPage')


keys = recordList[0].keys()
with open('assets_without_bibids.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(recordList)