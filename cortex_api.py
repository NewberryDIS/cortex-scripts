import requests
import config
from pprint import pprint as pp
import json


if __name__ == '__main__':

	authenticate_url = f'https://collections.newberry.org/API/Authentication/v1.0/Login?Login={config.username}&Password={config.password}&format=json'
	authenticate = requests.get(authenticate_url)

	token = authenticate.json()
	token = token['APIResponse']['Token']
	token = f'&token={token}'
	# pp(prefix)

	parent_folder = 'NL14CH4'
	parent_query = f"https://collections.newberry.org/API/search/v3.0/search?query=Title:'' AND ParentFolderIdentifier:{parent_folder}&fields=Title,MediaType,Identifier{token}&format=json"
	children = requests.get(parent_query)
	for child in children.json()['APIResponse']['Items']:
		system_identifier = child['Identifier']
		document_type = child['MediaType']
		child_record = requests.get(f'https://collections.newberry.org/API/DataTable/V2.2/Documents.{document_type}.Default:Read?CoreField.Identifier={system_identifier}{token}&format=json')
		child_record = child_record.json()
		pp(child_record)
		
		
			# identifier = 'NL15GSY'
			# child_record = requests.get(f'https://collections.newberry.org/API/DataTable/V2.2/Documents.All:Read?CoreField.Identifier={identifier}{token}&format=json')
			# pp(child_record)
		
			# ALL DOCUMENTS RETRIEVAL:
			# f'https://collections.newberry.org/API/DataTable/V2.2/Documents.All:Read?CoreField.Identifier={identifier}'
		
		 	# Folder URL: 
		 	# https://collections.newberry.org/API/DataTable/v2.2/Documents.Folder.Default:CreateOrUpdate?CoreField.Title={title}&CoreField.Parent-folder:=[Documents.Folder.Default:CoreField.Unique-Identifier=NL1CTB]
	
	# title = 'Claire'
	# test_create = requests.post(f'https://collections.newberry.org/API/DataTable/v2.2/Documents.Folder.Default:Create?CoreField.Title={title}{token}')


	# Parent folder: 
	# f'https://collections.newberry.org/API/search/v3.0/search?query=Title:'' AND ParentFolderIdentifier:{parent_folder}&fields=Title,Unique-Identifier,MediaType{token}'

