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

from addALMAdata import make_api_call

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


def resize_large_image(filepath):
	src = cv2.imread(filepath)
	scale_percent = 25
	width = int(src.shape[1] * scale_percent / 100)
	height = int(src.shape[0] * scale_percent / 100)

	dsize = (width, height)

	output = cv2.resize(src,dsize)

	cv2.imwrite(filepath, output)


def get_file_size(filepath):
	size = os.path.getsize(filepath)
	return size
	# pp(size)
	# if size > 2000000000:
	# 	return True
	# else:
	# 	return False


def check_for_stacking_rule(folder_path):
	first_file = os.listdir(folder_path)[0]
	if 'box' in first_file or 'bx' in first_file:
		rule = 'box'
		return rule
	else:
		rule = 'first_underscore'
		return rule


def create_error_dict(file, folder):
	d = {}
	d['filename'] = file
	d['folder'] = folder

	return d


def get_MediaEncryptedIdentifier(folder_id):
	folder_url = f'https://collections.newberry.org/API/search/v3.0/search?query=SystemIdentifier:{folder_id}&fields=MediaEncryptedIdentifier,ParentFolderTitle{token}{json_suffix}'
	req = requests.get(folder_url).json()
	mediaEncryptedIdentifier = req['APIResponse']['Items'][0]['MediaEncryptedIdentifier']
	return mediaEncryptedIdentifier	


def print_tracking(time_start, runningTotal, folder_count, file_count, fileSizeTotal, totalFiles):
	time_end = time.time()
	timeStop = datetime.datetime.fromtimestamp(time_end)
	str_time = timeStop.strftime("%d-%m-%Y %H:%M:%S")
	pp(f'Iteration ended at {str_time}')
	mostRecentLength = (time_end - time_start) / 60
	pp(f'Most recent (mins): {mostRecentLength}')
	runningTotalLength = (runningTotalLength + mostRecentLength) / 60 / 60
	pp(f'Total time (hours): {runningTotalLength}')
	runningAverage = (runningTotalLength / file_count) / 60
	pp(f'Average (mins): {runningAverage}')
	countRemaining = totalFiles - file_count
	timeTillComplete = countRemaining * runningAverage
	str_tillComplete = timeTillComplete.strftime("%d-%m-%Y %H:%M:%S")
	pp(f'Time till completion: {str_tillComplete}')
	newTime = time.time()
	estimatedCompletion = newTime + timeTillComplete
	str_estCompletion = estimatedCompletion.strftime("%d-%m-%Y %H:%M:%S")
	pp(f'Estimated completion: {str_estCompletion}')
	filesRemaining = totalFiles - file_count
	pp(f'Remaining files: {filesRemaining}')				
	pp(f'Total download size in bytes: {fileSizeTotal}')
	averageFileSize = (fileSizeTotal / file_count) / 1000000000
	pp(f'Average file size in GBs: {averageFileSize}')
	averageGBsPerMin = averageFileSize / runningAverage	
	pp(f'Average GBs per min: {averageGBsPerMin}')

	

if __name__ == '__main__':


	authenticate_url = f'https://collections.newberry.org/API/Authentication/v1.0/Login?Login={config.username}&Password={config.password}&format=json'
	authenticate = requests.get(authenticate_url)

	token = authenticate.json()
	token = token['APIResponse']['Token']
	token = f'&token={token}'
	json_suffix = '&format=json'

	# Creating ir folder generators
	box_folders = get_ia_folders('boxlib0')
	num_box_folders = len(box_folders)
	box_folder_gen = ia_folder_generator(box_folders)
	# pp(num_box_folders)
	# pp(box_folders)
	boxFolder = box_folder_gen.__next__()
	box_MediaEncryptedIdentifier = get_MediaEncryptedIdentifier(boxFolder)
	# pp(box_MediaEncryptedIdentifier)



	fund_folders = get_ia_folders('fundlib0')
	num_fund_folders = len(fund_folders)
	fund_folder_gen = ia_folder_generator(fund_folders)
	# pp(num_fund_folders)
	# pp(fund_folders)
	fundFolder = fund_folder_gen.__next__()
	# pp(fundFolder)
	fund_MediaEncrypedIdentifier = get_MediaEncryptedIdentifier(fundFolder)
	# pp(fund_MediaEncrypedIdentifier)

	## Tester
	# n = 40
	# while n > 0:
	# 	n = n - 1	
	# 	if (n % 15) == 0:
	# 		pp(fund_folder_gen.__next__())

	# Image Repository
	directory = '.'

	# Counting files
	totalFiles = 0
	for folder in os.listdir(directory):
		if folder[:2] == 'ur':
			for file in os.path.join(directory, folder):
				totalFiles += 1

	# Pulling from IR and uploading to Cortex
	data = []
	folder_count = 0
	box_folder_count = 0
	fund_folder_count = 0
	file_count = 0
	runningTotal = 0
	fileSizeTotal = 0
	for folder in os.listdir(directory): #1527
		time_start = time.time()
		# if folder[:2] == 'ur':
		if folder[:2] == 'xx'
			folder_count += 1
			pp(f'Folder {folder_count}')			
			pp(folder)
			folder_path = os.path.join(directory, folder)
			rule = check_for_stacking_rule(folder_path)
			if rule == 'box':
				box_folder_count += 1
				for file in os.listdir(folder_path):
					file_count += 1
					size = get_file_size(os.path.join(folder_path, file))
					fileSizeTotal = fileSizeTotal + size
					if size > 2000000000:
						file = resize_large_image(os.path.join(folder_path, file))
				
					# Upload
					try:
						files = {'UploadStream': open(os.path.join(folder_path, file), 'rb')}
						upload_req = f'https://collections.newberry.org/API/UploadMedia/v3.0/UploadNewMedia?FolderRecordID={box_MediaEncryptedIdentifier}&FileName={file}&UploadMode=ProcessFullyInBackground{token}{json_suffix}'
						r = requests.post(upload_req, files=files).json()
						resp_code = r['APIResponse']['Code']
						pp(resp_code)
						if resp_code == 'SUCCESS':
							# Insert metadata url here
							try:
								api_url = make_api_call(file, token, json_suffix)
								post_metadata = requests.post(api_url).json()
								pp(post_metadata)
							except Exception as e:
								pp(e)
					except Exception as e:
						data.append(create_error_dict(file, folder))
						pp(f'Error on {file}')
						pp(e)

				if (box_folder_count % 40) == 0:
					try:
						box_folder = box_folder_gen.__next__():
						box_MediaEncryptedIdentifier = get_MediaEncryptedIdentifier(box_folder)
						pp(f'Moving to new folder: {box_MediaEncryptedIdentifier}')
					except Exception as e:
						pp(e)

			elif rule == 'first_underscore':
				fund_folder_count += 1
				for file in os.listdir(folder_path):
					file_count += 1
					size = get_file_size(os.path.join(folder_path, file))
					fileSizeTotal = fileSizeTotal + size
					if size > 2000000000:
						file = resize_large_image(os.path.join(folder_path, file))

					# Upload
					try:
						files = {'UploadStream': open(os.path.join(folder_path, file), 'rb')}
						upload_req = f'https://collections.newberry.org/API/UploadMedia/v3.0/UploadNewMedia?FolderRecordID={fund_MediaEncrypedIdentifier}&FileName={file}&UploadMode=ProcessFullyInBackground{token}{json_suffix}'
						r = requests.post(upload_req, files=files).json()
						resp_code = r['APIResponse']['Code']
						if resp_code == 'SUCCESS':
							try:
								api_url = make_api_call(file, token, json_suffix)
								post_metadata = requests.post(api_url).json()
								pp(post_metadata)
							except Exception as e:
								pp(e)
					except Exception as e:
						data.append(create_error_dict(file, folder))
						pp(f'Error on {file}')
						pp(e)

				if (fund_folder_count % 200) == 0:
					try:
						fund_folder = fund_folder_gen.__next__():
						fund_MediaEncryptedIdentifier = get_MediaEncryptedIdentifier(fund_folder)
						pp(f'Moving to new folder: {fund_MediaEncryptedIdentifier}')
					except Exception as e:

			else:
				continue			

			# new_folder_name = folder.replace('ur', 'cu')
			new_folder_name = folder.replace('xx', 'cu')
			os.rename(folder_path, os.path.join(directory, new_folder_name))
			pp(f'Renaming {folder} to {new_folder_name}')
					

		# Tracking data
		print_tracking(time_start, runningTotal, folder_count, file_count, fileSizeTotal)



	# Generate error log
	keys = data[0].keys()
	with open('ir_ingest_errors.csv', 'w', newline='', errors='ignore', encoding='utf-8') as outfile:
		writer = csv.DictWriter(outfile, fieldnames=keys)
		writer.writeheader()
		writer.writerows(data['rows'])

	# Because of error stopping script, once everything is ingested, go back and get URLs that were skipped for containing files too big


	# time_end = time.time()
	# timeStop = datetime.datetime.fromtimestamp(time_end)
	# str_time = timeStop.strftime("%d-%m-%Y %H:%M:%S")
	# pp(f'Iteration ended at {str_time}')
	# mostRecent = (time_end - time_start) / 60
	# pp(f'Most recent (mins): {mostRecent}')
	# runningTotal = (runningTotal + mostRecent) / 60 / 60
	# pp(f'Total time (hours): {runningTotal}')
	# runningAverage = (runningTotal / folder_count) / 60
	# pp(f'Average (mins): {runningAverage}')
	# str_tillComplete = timeTillComplete.strftime("%d-%m-%Y %H:%M:%S")
	# pp(f'Time till completion: {str_tillComplete}')
	# newTime = time.time()
	# estimatedCompletion = newTime + timeTillComplete
	# str_estCompletion = estimatedCompletion.strftime("%d-%m-%Y %H:%M:%S")
	# pp(f'Estimated completion: {str_estCompletion}')			
	# pp(f'Total download size in bytes: {fileSizeTotal}')
	# averageFileSize = (fileSizeTotal / file_count) / 1000000000
	# pp(f'Average file size in GBs: {averageFileSize}')
	# averageGBsPerMin = averageFileSize / runningAverage	
	# pp(f'Average GBs per min: {averageGBsPerMin}')
