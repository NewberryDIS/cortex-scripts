import pandas as pd
from pprint import pprint as pp
import argparse
import config
import requests
import json
import time

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('search_filenames', nargs='?', help='CSV of all assets to be made into compound objects')
args = parser.parse_args()

# Authenticate session in Cortex
authenticate_url = f'https://collections.newberry.org/api/Authentication/v2.0/Login?Login={config.username}&Password={config.password}&IncludeUserEmail=false&format=json&api_key=authenticate'
authenticate = requests.post(authenticate_url)
# print(authenticate.text)

token = authenticate.json()
token = token['APIResponse']['Response']['Token']
token = f'&token={token}'
json_suffix = '&format=json'
pp('Authenticated!')

df = pd.read_csv(args.search_filenames, encoding='utf-8-sig')

column_name = 'Filename'

output_file_path = 'failed_call.txt'
success_file_path = "success_call.txt"
success_but_no_items = 'success_no_items_listed_all.txt'

all_files = []
for value in df['Filename']:
    api_url = f'https://collections.newberry.org/API/search/v3.0/search?query="{value}"mediatype:image&fields=Identifier,OriginalFileName{token}{json_suffix}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if "APIResponse" in data and "Items" in data["APIResponse"] and not data["APIResponse"]["Items"]:
            not_found = f"No items found for API call: {value}\n"
            with open(output_file_path, "a", encoding='utf-8-sig') as output_file:
                output_file.write(not_found)
        if "APIResponse" in data and "Items" in data["APIResponse"]:
            if data["APIResponse"]["Items"]:
                found_value = data["APIResponse"]["Items"][0]["OriginalFileName"]
                found = f"Searched {value}: found {found_value}\n"
                with open(success_file_path, "a", encoding='utf-8-sig') as success_file:
                    success_file.write(found)
            else:
                with open(success_but_no_items, "a", encoding='utf-8-sig') as no_items_files:
                    no_items_files.write(f"No items found in the list for {value}\n")

end = time.time()
totalIterationTime = end - start
totalIterationTime = totalIterationTime / 60
pp(f'Time to search Cortex (mins): {totalIterationTime}')