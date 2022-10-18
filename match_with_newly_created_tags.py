import csv
from pprint import pprint as pp
import argparse
import pandas as pd
import re

parser = argparse.ArgumentParser()
parser.add_argument('csv1', nargs='?', help='CSV of tags to be replaced')
parser.add_argument('tagTree', nargs='?', help='CSV of all tags--must be newly generated TagTree to reflect tags made in Step 1')
parser.add_argument('tagType', nargs='?', help='Type of tag working with')
args = parser.parse_args()


# Does pretty much the same as check_if_tag_already_exists, but instead of caring about DELETE, only cares about tags that still need matches


def check_for_tag(allTagsDict, tag):
	for k, v in allTagsDict.items():
		if v == tag.strip():
			return k


def check_for_id(allIdsList, orig_tag):
	tag_id = orig_tag.split('_')[1].strip()
	if tag_id in allIdsList:
		return True
	else:
		pp(f'Tag already deleted: {orig_tag}')
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



allTagKeys = tags[0].keys()


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
				get_tag = check_for_tag(allTags, row['Correct_Tag']) # Checks to see if correct_tag already exists; if so, creates template row replacing old tag with it
				if get_tag != None:
					count += 1
					pp(count)
					# pp(k)
					d['KeyType'] = args.tagType
					d['ReplaceBy'] = get_tag
					d['Level0_Label'] = row['Level0_Label']
					d['Facet_Category_Code'] = f'{args.tagType}_Filter'
					pp(f'{d["Level0_Label"]} to be replaced by {d["ReplaceBy"]}')
					rows.append(d)
		else:
			continue
			# count += 1
			# pp(count)
			# pp(row)

pp(len(rows))

keys = rows[0].keys()
with open('tags_to_replace.csv', 'w', encoding='utf-8', errors='ignore', newline='') as outfile:
	writer = csv.DictWriter(outfile, keys)
	writer.writeheader()
	writer.writerows(rows)