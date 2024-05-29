from pprint import pprint as pp
import argparse
import csv
import re
import os


def html_catalog_link(catalog_link):
	# pp(catalog_link)
	if catalog_link	!= '':
		# link = re.findall(r"https://(.*?)>View", catalog_link)
		# pp(link)
		if 'a href' not in catalog_link:
			catalog_link = f'<a href={catalog_link} target="_blank">View record</a>'
			# pp(catalog_link)

	return catalog_link


def html_disclaimer_stmt(disclaimer_stmt):
	link = '<a href="https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf">More information</a>'
	disclaimer_stmt	= disclaimer_stmt.replace('More information: https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf', link)
	return disclaimer_stmt


def html_oa_policy(oa_policy):
	new_oa_policy = 'The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to these <a href="https://www.newberry.org/rights-and-reproductions">terms and conditions</a>.'	
	return new_oa_policy


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('directory', help='directory')
	args = parser.parse_args()


	# catalog_link = 'https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma992974798805867'
	# disclaimer = 'All materials in the Newberry Library’s collections have research value and reflect the society in which they were produced. They may contain language and imagery that are offensive because of content relating to: ability, gender, race, religion, sexuality/sexual orientation, and other categories. More information: https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf'
	# oa_policy = 'The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to the following terms and conditions: https://www.newberry.org/rights-and-reproductions'
	# pp(html_catalog_link(catalog_link))
	# pp(html_disclaimer_stmt(disclaimer))
	# pp(html_oa_policy(oa_policy))

	
	for filename in os.listdir(args.directory):
		rows = []
		f = os.path.join(args.directory, filename)
		with open(f, encoding='utf-8', errors='ignore') as csv_file:
			reader = csv.DictReader(csv_file)
			for row in reader:
				row['CATALOG_LINK'] = html_catalog_link(row['CATALOG_LINK'])
				pp(row['CATALOG_LINK'])
				row['DISCLAIMER_STMT'] = 'All materials in the Newberry Library\'s collections have research value and reflect the society in which they were produced. They may contain language and imagery that are offensive because of content relating to: ability, gender, race, religion, sexuality/sexual orientation, and other categories. <a href="https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf">More information</a>'
				pp(row['DISCLAIMER_STMT'])
				row['OA_POLICY'] = html_oa_policy(row['OA_POLICY'])
				pp(row['OA_POLICY'])
				rows.append(row)
		# pp(rows)
		if len(rows) != 0:
			keys = rows[0].keys()
			with open(f, 'w', newline='', encoding='utf-8', errors='ignore') as outfile:
					dict_writer = csv.DictWriter(outfile, keys)
					dict_writer.writeheader()
					dict_writer.writerows(rows)

		# <a href="url">link text</a>