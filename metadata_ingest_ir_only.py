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

import time
import argparse

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

import logging

from addALMAdata import generate_metadata_dict

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


spreadsheet_id = '1EiJWmJqK3Z4-bUjS52HlcrN6gVZauN2tdPyarMelWwU'
range_ = 'A:A'
sheet = sheets_service.spreadsheets()



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


def check_field_length(filename):
	i = generate_metadata_dict(filename)
	# logging.info(i)
	for k, v in i.items():
		if k != 'DISCLAIMER_STMT':
			if len(v) > 300:
				logging.error(f'Field too long {k}')
				return filename

	return i


def make_api_call(metadata_dict, token, json_suffix):

    # i = generate_metadata_dict(filename)
    i = metadata_dict
    url = f'''https://collections.newberry.org/API/DataTable/V2.2/Documents.Image.Default:Update?
        Corefield.OriginalFileName={i['FILENAME']}
        &CoreField.title:={i['TITLE']}
        &CoreField.description:={i['DESCRIPTION']}
        &new.Date-Created:={i['DATE_DISPLAY']}
        &new.Sort-Date:={i['DATE_SORT']}
        &new.Place++={i['PLACE']}
        &new.Source-/-Creator++={i['CREATOR']}
        &new.Publisher++={i['PUBLISHER_ORIGINAL']}
        &new.Subject++={i['SUBJECTS']}
        &new.Contributing-Institution+:={i['CONTRIBUTING_INSTITUTION']}
        &new.Format++={i['FORMAT']}
        &new.DCMI-Type++={i['DCMIType']}
        &new.Extent:={i['FORMAT_EXTENT']}
        &new.Language++={i['LANGUAGE']}
        &new.Archival-Collection-Title++={i['ARCHIVAL_COLLECTION']}
        &new.Catalog-Record-/-Collection-Guide:={i['CATALOG_LINK']}
        &new.Biographical/Historical-Note-Long:={i['BIOGRAPHICAL/HISTORICAL NOTE']}
        &new.Summary-Long:={i['SUMMARY']}
        &CoreField.Purpose:=PendingProcess
        &new.Rights-Status+:={i['STANDARDIZED_RIGHTS']}
        &new.Call-Number:={i['CALL_NUMBER']}
        &new.BibID-Link+:={i['BIBID']}
        &new.Newberry-Open-Access-Policy+:={i['OA_POLICY']}
        {token}
        {json_suffix}'''
    logging.info(url)

    return url


def print_tracking(time_start, runningTotal, folder_count, file_count, fileSizeTotal, totalFiles, runningTotalLength):
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


	logging.basicConfig(level=logging.INFO)

	# parser = argparse.ArgumentParser(description='')
	# parser.add_argument('time_run', help='num of secs for script to run')
	# parser.add_argument('outfile', help='csv of alma data')
	# args = parser.parse_args()

	# Length of time for script to run
	# max_time = int(args.time_run)

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
	fund_MediaEncryptedIdentifier = get_MediaEncryptedIdentifier(fundFolder)
	# pp(fund_MediaEncryptedIdentifier)

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
	ir_folders_with_too_long_fields = []
	successful_metadata_ingest = []
	folder_count = 0
	box_folder_count = 0
	fund_folder_count = 0
	file_count = 0
	runningTotal = 0
	fileSizeTotal = 0
	runningTotalLength = 0
	successful_metadata_posts = 0
	unsuccessful_metadata_posts = 0

	# Create output metadata files
	fields = ['folder']	 
	if os.path.isfile('successful_metadata_ingests.csv') == False:
		with open('successful_metadata_ingests.csv', 'w', errors='ignore', encoding='utf-8', newline='') as outfile:
			writer = csv.DictWriter(outfile, fieldnames = fields)
			writer.writeheader()

	if os.path.isfile('ir_folders_with_too_long_fields.csv') == False:
		with open('ir_folders_with_too_long_fields.csv', 'w', errors='ignore', encoding='utf-8', newline='') as outfile:
			writer = csv.DictWriter(outfile, fieldnames = fields)
			writer.writeheader()


	# Main code
	for folder in os.listdir(directory): #1527
		# pp(folder)
		time_start = time.time()
		if folder[:2] == 'ur':
		# if folder[:2] == '*xx':
			folder_count += 1
			logging.info(f'Folder {folder_count}')			
			# pp(folder)
			folder_path = os.path.join(directory, folder)
			rule = check_for_stacking_rule(folder_path)
			logging.info(f'{rule}')
			if rule == 'box':
				box_folder_count += 1
				logging.info(f'Ingesting to folder: {box_MediaEncryptedIdentifier}')
				for file in os.listdir(folder_path):
					try:
						length_check = check_field_length(file)
						typ = type(length_check)
						logging.debug(typ)
						# logging.error('Length check')
						# logging.error(length_check)
						if type(length_check) == dict:
							try:
								api_url = make_api_call(length_check, token, json_suffix)
								logging.error(f'{api_url}')
								post_metadata = requests.post(api_url).json()
								logging.info(post_metadata)
								successful_metadata_posts += 1
								if folder not in successful_metadata_ingest:
									successful_metadata_ingest.append(folder)
									data = []
									d = {}
									d['folder'] = folder
									data.append(d)
									with open('successful_metadata_ingest.csv', 'a', newline='', encoding='utf-8') as outfile:
										writer = csv.DictWriter(oufile, fieldnames = fields)
										writer.writerows(data)
							except KeyError:
								logging.error(length_check, exc_info=True)

						elif type(length_check) == str:
							unsuccessful_metadata_posts += 1
							if folder not in ir_folders_with_too_long_fields:
								ir_folders_with_too_long_fields.append(folder)
								data = []
								d = {}
								d['folder'] = folder
								data.append(d)
								with open('ir_folders_with_too_long_fields.csv', 'a', errors='ignore', encoding='utf-8', newline='') as outfile:
									writer = csv.DictWriter(outfile, fieldnames = fields)
									writer.writerows(data)
					except Exception as e:
						# data.append(create_error_dict(file, folder))
						logging.error(f"Exception occurred for {file}", exc_info=True)

				if (box_folder_count % 40) == 0:
					try:
						box_folder = box_folder_gen.__next__()
						box_MediaEncryptedIdentifier = get_MediaEncryptedIdentifier(box_folder)
						logging.info(f'Moving to new folder: {box_MediaEncryptedIdentifier}')
					except Exception as e:
						logging.error("Exception occurred switching Cortex folders", exc_info=True)

			elif rule == 'first_underscore':
				fund_folder_count += 1
				logging.info(f'Ingesting to folder: {fund_MediaEncryptedIdentifier}')
				for file in os.listdir(folder_path):
					logging.info(f'{file}')
					file_count += 1
					try:
						length_check = check_field_length(file)
						typ = type(length_check)
						logging.info(typ)
						# logging.error('Length check')
						# logging.error(length_check)
						if type(length_check) == dict:
							try:
								api_url = make_api_call(length_check, token, json_suffix)
								logging.debug(f'{api_url}')
								post_metadata = requests.post(api_url).json()
								logging.info(post_metadata)
								successful_metadata_posts += 1
								if folder not in successful_metadata_ingest:
									successful_metadata_ingest.append(folder)
									data = []
									d = {}
									d['folder'] = folder
									data.append(d)
									with open('successful_metadata_ingest.csv', 'a', newline='', encoding='utf-8') as outfile:
										writer = csv.DictWriter(oufile, fieldnames = fields)
										writer.writerows(data)
							except KeyError:
								logging.error(length_check, exc_info=True)
						elif type(length_check) == str:
							unsuccessful_metadata_posts += 1
							if folder not in ir_folders_with_too_long_fields:
								ir_folders_with_too_long_fields.append(folder)
								data = []
								d = {}
								d['folder'] = folder
								data.append(d)
								with open('ir_folders_with_too_long_fields.csv', 'a', errors='ignore', encoding='utf-8', newline='') as outfile:
									writer = csv.DictWriter(outfile, fieldnames = fields)
									writer.writerows(data)
					except Exception as e:
						# data.append(create_error_dict(file, folder))
						logging.error(f"Exception occurred for {file}", exc_info=True)


				if (fund_folder_count % 200) == 0:
					try:
						fund_folder = fund_folder_gen.__next__()
						fund_MediaEncryptedIdentifier = get_MediaEncryptedIdentifier(fund_folder)
						logging.info(f'Moving to new folder: {fund_MediaEncryptedIdentifier}')
					except Exception as e:
						logging.error("Exception occurred switching Cortex folders", exc_info=True)

			else:
				continue			

					

			# Tracking data
			time_end = time.time()
			timeStop = datetime.datetime.fromtimestamp(time_end)
			str_time = timeStop.strftime("%d-%m-%Y %H:%M:%S")
			pp(f'Iteration ended at {str_time}')
			mostRecentLength = (time_end - time_start) 
			pp(f'Most recent: {mostRecentLength}')
			runningTotalLength = runningTotalLength + mostRecentLength
			pp(f'Total time: {runningTotalLength}')
			runningAverage = runningTotalLength / folder_count
			pp(f'Average: {runningAverage}')
			countRemaining = totalFiles - file_count
			pp(f'Files remaining: {countRemaining}')
			pp(f'Successful metadata ingests: {successful_metadata_posts}')
			pp(f'Unsuccessful metadata ingests: {unsuccessful_metadata_posts}')
			

			# timeTillComplete = countRemaining * runningAverage
			# str_tillComplete = timeTillComplete.strftime("%d-%m-%Y %H:%M:%S")
			# pp(f'Time till completion: {timeTillComplete}')
			# newTime = time.time()
			# estimatedCompletion = int(newTime + timeTillComplete)
			# str_estCompletion = estimatedCompletion.strftime("%d-%m-%Y %H:%M:%S")
			# pp(f'Estimated completion: {estimatedCompletion}')
			# filesRemaining = totalFiles - file_count
			# pp(f'Remaining files: {filesRemaining}')				
			# pp(f'Total download size in bytes: {fileSizeTotal}')
			# averageFileSize = (fileSizeTotal / file_count) / 1000000000
			# pp(f'Average file size in GBs: {averageFileSize}'
			# averageGBsPerMin = averageFileSize / runningAverage
			# pp(f'Average GBs per min: {averageGBsPerMin}')



