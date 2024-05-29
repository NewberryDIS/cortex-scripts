import httplib2

# from move_cataloged_assets import move_to_folder

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
# from Google import Create_Service
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery
from pprint import pprint as pp

import requests
import os
import config
import wget
import zipfile
import stat
import time
import shutil
import csv
import datetime
import cv2
import tarfile

ct = datetime.datetime.now()
timestamp = ct.strftime("%m-%d-%Y, %H:%M:%S")
# pp(timestamp)

# If modifying these scopes, delete the file token.json.
CLIENT_SECRETS_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/drive", 
          "https://www.googleapis.com/auth/drive.file", 
          "https://www.googleapis.com/auth/spreadsheets"]
          


secret_file = os.path.join(os.getcwd(), 'credentials.json')
credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
sheets_service = discovery.build('sheets', 'v4', credentials=credentials)
drive_service = discovery.build('drive', 'v3', credentials=credentials)


def check_moveFolder_less_than_50000(folder):
	url = f'https://collections.newberry.org/API/search/v3.0/search?query=OriginalSubmissionNumber:{folder}&fields=SystemIdentifier,Title,OriginalFilename,ParentFolderTitle{token}{json_suffix}'
	get_folder = requests.get(url)
	folder_response = get_folder.json()
	if folder_response['APIResponse']['GlobalInfo']['TotalCount'] < 50001:
		return True
	else:
		return False


def get_ia_folders(folder_stem):
	query = f'https://collections.newberry.org/API/search/v3.0/search?query=DocSubType:Standard Folder&fields=Title,SystemIdentifier{token}{json_suffix}'
	response = requests.get(query).json()
	lib_folders = {}
	for item in response['APIResponse']['Items']:
		if folder_stem in item['Title']:
			tup = (item['Title'], item['SystemIdentifier'])
			lib_folders[item['Title']] = item['SystemIdentifier']
	folder_titles = list(lib_folders.keys())
	folder_titles.sort(reverse=False)
	return lib_folders


def ia_folder_generator(lib_folders):
	for s in list(lib_folders.keys()):
		yield lib_folders.get(s)


# def check_file_sizes(url, bibid, path):
# 	file_sizes_smaller_than_2GBs = True
# 	for f in os.listdir(path):
# 		size = os.path.getsize(os.path.join(path,f))
# 		if size > 2000000:
# 			return (url, bibid)
# 		else:
# 			continue
# 	return file_sizes_smaller_than_2GBs


def resize_large_image(filepath):
	src = cv2.imread(filepath)
	scale_percent = 25
	width = int(src.shape[1] * scale_percent / 100)
	height = int(src.shape[0] * scale_percent / 100)

	dsize = (width, height)

	output = cv2.resize(src,dsize)

	cv2.imwrite(filepath, output)


def check_file_size_too_big(filepath):
	size = os.path.getsize(filepath)
	pp(size)
	if size > 2000000:
		return True
	else:
		return False



if __name__ == '__main__':


	# IA_Left_To_Add
	sheet_id = '1LnfpIaBhHdl-ng6V-ZDBXFMuY1nFzXAJL7M1jaGCoDQ'
	range_name = "A:B"  
	response = sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()


	fails = []
	total_count = len(response['values'][1:])
	count = 0
	for value in response['values'][1:]:
		url = value[0]
		bibid = value[1]

		download = False
		try:
			wget.download(url)
			download = True
		except Exception as e:
			f = {}
			pp(e)
			pp(url)
			f['url'] = value[0]
			f['bibid'] = value[1]
			fails.append(f)
			continue

		if download == True:
			folder_name_1 = url.split('/')[-1]
			folder_name_2 = folder_name_1.replace('.zip', '')

			try:
				count += 1
				start = time.time()
				with zipfile.ZipFile(f'{folder_name_1}', 'r') as zip_ref:
					zip_ref.extractall(f'.')
				os.remove(folder_name_1)
				for file in os.listdir(folder_name_2):
					new_file_name = bibid + '_' + file
					os.rename(os.path.join(folder_name_2, file), os.path.join(folder_name_2, new_file_name))
				end = time.time()
				total = end = start
				pp(f"{url} took {total} seconds")
				remaining = total_count	- count
				pp(f'{remaining} urls to download')
			except Exception as e:
				pp(e)
				f = {}
				pp(url)
				f['url'] = value[0]
				f['bibid'] = value[1]
				fails.append(f)

	try:
		keys = fails[0].keys()
		with open('fails.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
			writer = csv.DictWriter(outfile, fieldnames=keys)
			writer.writeheader()
			writer.writerows(fails)		
	except IndexError:
		pp('No errors')	


	# Because of error stopping script, once everything is ingested, go back and get URLs that were skipped for containing files too big