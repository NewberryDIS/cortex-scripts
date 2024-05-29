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
import logging
import socket

# Define the formatter and configure the logging module with the formatter
formatter = logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=formatter)

# retry network requests
def make_request_with_retries(url, max_retries=3, delay=1):
	retries = 0
	while retries < max_retries:
		try:
			response = requests.get(url)
			if response.status_code == 200:
				return response.json()
			else:
				logging.error(f'Error: received status code {response.status_code}')
		except requests.exceptions.RequestException as e:
			logging.error(f'Error: {e}')
		
		retries += 1
		print(f"Retrying ({retries}/{max_retries})...")
		time.sleep(delay)

	print("Max retries exceed. Unable to complete request.")
	return None

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
authenticate_url = f'https://collections.newberry.org/api/Authentication/v2.0/Login?Login={config.username}&Password={config.password}&IncludeUserEmail=false&format=json&api_key=authenticate'
authenticate = requests.post(authenticate_url)
# print(authenticate.text)

token = authenticate.json()
token = token['APIResponse']['Response']['Token']
token = f'&token={token}'
json_suffix = '&format=json'
pp('Authenticated!')

### If passing a spreadsheet as an argument, the spreadsheet needs two columns titled this: BIBID and FILENAME

if '.csv' in folders[0]:    
	for c in folders:
		with open(c, encoding='utf-8', errors='ignore') as csv_:
			reader = csv.DictReader(csv_)
			# pp(keys)
			for row in reader:
				# pp(row.keys()) ## If getting 'KeyError', uncomment this line and run script to see if encoding issues have warped the first column heading into something like: ''. 
				## If so, you will need to paste that column heading into the matching one below
				bibid_dict = {}
				bibid_dict['FILENAME'] = row['FILENAME']
				bibid_dict['BIBID'] = row['\ufeffBIBID']
				recordList.append(bibid_dict)
				# pp(recordList)

else:
	for folder in folders:
		url = f'https://collections.newberry.org/API/search/v3.0/search?query=OriginalSubmissionNumber:{folder}&fields=SystemIdentifier,Title,OriginalFilename,ParentFolderTitle,CoreField.Purpose{token}{json_suffix}'
		get_folder = requests.get(url)
		# print('HTTP Status Code:', get_folder.status_code)
		folder_response = get_folder.json()
		if folder_response:
			total = folder_response['APIResponse']['GlobalInfo']['TotalCount']
			# pp(total)
			items = folder_response['APIResponse']['Items']
			# pp(items)
			for item in items:
				if item['CoreField.Purpose'] == 'Public' or item['CoreField.Purpose'] == 'Pending process':
					if item['OriginalFilename'].strip()[:4].isdigit() == True:
						# pp(f'Getting data for: {item["OriginalFilename"]}')
						bibid_dict = af.get_bibid_dict(item['OriginalFilename'])
						recordList.append(bibid_dict)
			nextPage = folder_response['APIResponse']['GlobalInfo'].get('NextPage')
			while nextPage != None:
				get_folder = requests.get(f'{nextPage["href"]}{json_suffix}')
				folder_response = get_folder.json()
				for item in folder_response['APIResponse']['Items']:
					if item['CoreField.Purpose'] == 'Public' or item['CoreField.Purpose'] == 'Pending process':
						if item['OriginalFilename'].strip()[:4].isdigit() == True: 
							# pp(f'Getting data for: {item["OriginalFilename"]}')
							bibid_dict = af.get_bibid_dict(item['OriginalFilename'])
							recordList.append(bibid_dict)
				nextPage = folder_response['APIResponse']['GlobalInfo'].get('NextPage')


records_count = len(recordList)
pp(f'Getting data for {records_count} records')
pp(recordList)


items = []
count = 0
for i in recordList:
	count += 1
	# pp(count)
	# this particular item's data; will be pushed into items
	itemDict = af.set_dict()

	# run holdings record to grab the properly formatted Call Number
	if len(i['BIBID']) > 8:
		holdingsURL = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/' + str(i['BIBID']) + '/holdings?apikey=' + apikey
	else:
		holdingsURL = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/99' + str(i['BIBID']) + '8805867/holdings?apikey=' + apikey
	timeout = 10
	print(holdingsURL)
	try:
		# itemData = urllib.request.urlopen(itemUrl)
		with urllib.request.urlopen(holdingsURL, timeout=timeout) as holdingsData:
			print('HTTP Status Code:', holdingsData.getcode())
			parsedXml = ET.parse(holdingsData)
			root = parsedXml.getroot()
			# pp('Root')
			# pp(root)
			# Extract call_number
			try:
				call_number = root.find('.//call_number').text
				itemDict['CALL_NUMBER'] = call_number
			except Exception as e:
				logging.error(f"An error occured while retrieving the call number:", e)
	except urllib.error.URLError as e:
		print("Error", e)
	except socket.timeout:
		print("Error: Request timed out")
			
	# if items already has an item with this bibid in it, then we copy all data from that one, changing only the filename; 
	# this approach becomes problematic in cases like the Akwesasne notes where the bibid may have other changing values, like dates
	# alreadyDoneIndex = next((index for (index, d) in enumerate(items) if len(items) > 0 and 'BIBID' in d and d['BIBID'] == i['BIBID']), None)
	# if alreadyDoneIndex != None:
	#     # copy entire item
	#     itemDict = dict(items[alreadyDoneIndex])
	#     # pp('Already done')
	#     # pp(itemDict)
	#     # change filename in new one
	#     # if item['OriginalFilename'].strip()[:4].isdigit() == True: 
	#     #     itemDict['FILENAME'] = i['FILENAME']
	#     # else:
	#     #     itemDict['FILENAME'] = i['BIBID'] + '_' + i['FILENAME']
	#     # pp(itemDict['TITLE'])
	#     items.append(itemDict)
	# if this bibid isn't already in items, it goes through the full process; ie, this is the bulk of the script
	# else: 
	# using length to if bibid already has the 99/8805867 pre- and suffix 
	# sample url: https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs?mms_id=998600358805867&view=full&expand=None&apikey=xxxd
	if len(i['BIBID']) > 8: 
		itemUrl = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs?mms_id=' + str(i['BIBID']) + '&view=full&expand=None&apikey=' + apikey 
	else: 
		itemUrl = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs?mms_id=99' + str(i['BIBID']) + '8805867&view=full&expand=None&apikey=' + apikey 
	print(itemUrl)
	timeout = 10
	try: 
		# itemData = urllib.request.urlopen(itemUrl)
		with urllib.request.urlopen(itemUrl, timeout=timeout) as itemData:
			# print('HTTP Status Code:', itemData.getcode())
			parsedXml = ET.parse(itemData)
			root = parsedXml.getroot()
			# pp('Root')
			# pp(root)
	except urllib.error.URLError as e:
		print("Error", e)
	except socket.timeout:
		print("Error: Request timed out")
	# except Exception as e: 
	# 	root = ''
	# 	logging.error(f'An error occured when accessing the API: {e}')

	# if the data returned has a root value, we continue; if it doesn't, it's dumped into the reject pile
	if len(root) > 0:

		itemDict['BIBID'] = af.strip_bibid(i['BIBID'])
		itemDict['FILENAME'] = i['FILENAME']
		# itemDict['FILENAME'] =  i['BIBID'] + '_' + i['FILENAME']
		itemDict['TITLE'] = '' if root[0].find('title') is None else af.titleFormatter(root[0].find('title').text)
		# same length test as above
		if len(i['BIBID']) > 8: 
			itemDict['CATALOG_LINK'] = f"<a href='https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma{str(i['BIBID'])}'' target='_blank'>View record</a>"
		else: 
			itemDict['CATALOG_LINK'] = f"<a href='https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma99{str(i['BIBID'])}8805867' target='_blank'>View record</a>"           
		   
		records = root[0].find('record')
		# for record in root[0].find('record'):
		if records is not None:
			for record in records:
				# link to crosswalk:
				# https://docs.google.com/spreadsheets/d/1etIvF5Vjn1kty51qevsZ9mlWTOl_U9p_iCzWk_WOP9M/edit#gid=1296018796
											
				marcCode = record.get('tag')
				# pp(marcCode)
				af.valueAssignmentFromCode(itemDict, record, marcCode)
					
				# resolving lists created by multiple marc codes
				if ('PLACE' not in itemDict or len(itemDict['PLACE']) == 0) and len(itemDict['PLACE_list']) > 0: 
					itemDict['PLACE'] = af.resolveList(itemDict['PLACE_list'])
				if ('SUBJECTS' not in itemDict or len(itemDict['SUBJECTS']) == 0) and len(itemDict['SUBJECTS_list']) > 0: 
					itemDict['SUBJECTS']  = af.resolveList(itemDict['SUBJECTS_list'])
				if ('FORMAT' not in itemDict or len(itemDict['FORMAT']) == 0) and len(itemDict['FORMAT_list']) > 0: 
					itemDict['FORMAT']  = af.resolveList(itemDict['FORMAT_list'])
		else:
			print('No records found.')

		# remove format-helping values
		# del itemDict['SUBJECTS_list']
		# del itemDict['PLACE_list']
		# del itemDict['FORMAT_list']
		# del itemDict['ARCHIVAL_COLLECTION_list']
		# reviewSet.append(itemDict)
			

		itemDict = af.processStandardizedRights(itemDict)
		itemDict = af.processTitle(itemDict)
		# itemDict = af.remove_article_from_title(itemDict)
		itemDict = af.processArchivalCollection(itemDict)
		itemDict["DATE_SORT"] = itemDict["DATE_SORT"] + '-01-01'
		# pp(itemDict['TITLE'])
		# pp(itemDict['SUBJECTS'])
		# pp(itemDict['FORMAT'])
		# pp(itemDict['TITLE'])
		# pp(itemDict['CALL_NUMBER'])
		items.append(itemDict)

dataFilename = f'Central_{today}_data_recent_uploads.csv'


print("length of item array: " + str(len(items)))
if len(items) > 0:
	keys = items[0].keys()
	with open(dataFilename, 'w', newline='', errors='ignore', encoding='utf-8-sig')  as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(items)
		pp(f'Wrote spreadsheet: {output_file}')
else: 
	print("Big error.  Items array was length = 0")


end = time.time()
totalIterationTime = end - start
totalIterationTime = totalIterationTime / 60
pp(f'Time to download metadata (mins): {totalIterationTime}')



