import csv
import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('ArchivesSpace_resource_ID', nargs='*')
args = parser.parse_args()
ArchivesSpace_resource = args.ArchivesSpace_resource_ID

#Set your authentication info, baseurl, and repository info (if relevant)
baseURL = 'https://newberry-api.as.atlas-sys.com' #<-- Enter your real API URL between the ''
user = 'dearcangelisa' #<-- Enter your real username between the ''
password = 'Walter87@NL' #<-- Enter your real password between the ''

#Authorize and store your session key in your header
auth = requests.post(baseURL + '/users/' + user + '/login?password=' + password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

print('Your session key is: ' + session)

#Optional way to create your endpoint with variable below
# record_type = 'resources'

endpoint = '/repositories/2/resources/' + '/'.join(ArchivesSpace_resource) + '/ordered_records'

test_endpoint = requests.get(baseURL + endpoint, headers=headers) #Here we begin to test your endpoint, this is good to know
if test_endpoint.status_code !=200: #If the status code is NOT 200, your GET above did not work and the script stops
    print('That did not work. Do you have the correct endpoint? --> ' + endpoint)
    quit()
else: #If the status code IS 200, your GET above did work and the script continues
    archival_object = requests.get(baseURL + endpoint, headers=headers).json()

# with open('archival_object.json', 'w') as json_file:
#     json.dump(archival_object, json_file)

# with open('archival_object.json', 'r') as json_file:
#     arch_obj_file = json.load(json_file)

refs = [item['ref'] for item in archival_object['uris']]
# print(refs)

all_arch_objs = []
for ref in refs:
    # print(baseURL + ref)
    response = requests.get(baseURL + ref, headers=headers).json()
    # if response.status_code !=200:
    #     print('Error')
    # each_obj = json.loads(response.text)
    # print(each_obj)
    all_arch_objs.append(response)

with open('all_archival_obj_info.json', 'w') as new_file:
    json.dump(all_arch_objs, new_file)