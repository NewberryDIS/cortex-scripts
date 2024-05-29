import requests
import os
import config
from pprint import pprint as pp




if __name__ == '__main__':


	authenticate_url = f'https://collections.newberry.org/API/Authentication/v1.0/Login?Login={config.username}&Password={config.password}&format=json'
	authenticate = requests.get(authenticate_url)

	token = authenticate.json()
	token = token['APIResponse']['Token']
	token = f'&token={token}'
	json_suffix = '&format=json'


	folder_url = f'https://collections.newberry.org/API/DataTable/V2.2/Documents.Virtual-Folder.Compound-Object---Text:ListFields{token}{json_suffix}'
	req = requests.get(folder_url).json()
	fields = list(req['Response'].keys())


	with open('cortexcot_fields.txt', 'w') as outfile:
		for f in fields:
			outfile.write(f)
			outfile.write('\n')

