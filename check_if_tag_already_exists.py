import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re

parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of tags to be replaced')
parser.add_argument('tagTree', nargs='?', help='CSV of all tags')
parser.add_argument('tagType', nargs='?', help='Type of tag working with')
args = parser.parse_args()



# Checks to see if tags to be replaced already exist. If not, creates template spreadsheet for their creation or deletion or replacement, as indicated by Jessica's spreadsheet




def check_for_tag(allTagsDict, tag):
	for k, v in allTagsDict.items():
		if v == tag.strip():
			return k


def check_for_id(allIdsList, orig_tag):
	try:
		tag_id = orig_tag.split('_')[1].strip()
		if tag_id in allIdsList:
			return True
		else:
			pp(f'Tag already deleted: {orig_tag}')
			return False
	except IndexError:
		pp(orig_tag)
		return False




allTags = {}
allIds = []
tags = []
with open(args.tagTree, encoding='utf-8', errors='ignore') as csv_:
	reader = csv.DictReader(csv_)
	for row in reader:
		tags.append(row)
		# pp(row['Level0_Label'].split('_'))
		tag_ = row['Level0_Label'].split('_')[0].strip()
		allTags[row['Level0_Label']] = tag_
		try:
			tag_id = row['Level0_Label'].split('_')[1].strip()
			if tag_id not in allIds: allIds.append(tag_id)
		except IndexError:
			continue
			# pp(row)

# pp(allTags)
# pp(allIds)

allTagKeys = tags[0].keys()
pp(allTagKeys)

rows = []
count = 0
with open(args.csv1, encoding='utf-8', errors='ignore') as csv1_:
	reader = csv.DictReader(csv1_)
	for row in reader:
		if row['Correct_Tag'] != '' and 'ignore' not in row['Correct_Tag']:
			# Check first if original tag exists at all, considering how many we've deleted since I created these lists for Jessica
			tag_check = check_for_id(allIds, row['Level0_Label'])
			# pp(tag_check)
			if tag_check == True:
				d = {key: '' for key in allTagKeys}
				if 'delete' in row['Correct_Tag'].lower(): 
					# count += 1
					# pp(count)
					# pp(row['Tag'])
					d['KeyType'] = args.tagType
					d['Level0_Label'] = row['Level0_Label']
					d['Delete_Y_N'] = 'Y'
					rows.append(d)

				else:
					get_tag = check_for_tag(allTags, row['Correct_Tag']) # Checks to see if correct_tag already exists; if so, creates template row replacing old tag with it
					if get_tag != None:
						# count += 1
						# pp(count)
						# pp(k)
						d['KeyType'] = args.tagType
						d['ReplaceBy'] = get_tag
						d['Facet_Category_Code'] = f'{args.tagType}_Filter'
						d['Level0_Label'] = row['Level0_Label']
						pp(f'{d["Level0_Label"]} replaced by {d["ReplaceBy"]}')
						# pp(d)
						rows.append(d)
					else: # If tag doesn't already exist, creates template row for its creation
						d['KeyType'] = args.tagType
						d['Level0_Label'] = row['Correct_Tag']
						d['Facet_Category_Code'] = f'{args.tagType}_Filter'
						d['TreeLevel'] = '0'
						d['MultipleAssignment'] = 'FALSE'
						d['NotSearchable'] = 'FALSE'
						d['ToBeVetted'] = 'FALSE'
						pp(f'Creating {d["Level0_Label"]}')
						# pp(d)
						rows.append(d)
			else:
				continue
				# count += 1
				# pp(count)
				# pp(row)

pp(len(rows))

keys = rows[0].keys()
with open('tag_to_delete_or_replace_or_create.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)



