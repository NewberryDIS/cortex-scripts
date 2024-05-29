from pprint import pprint as pp
import argparse
import csv
import re


def pad_box_no(filename):
	# _012
	box = re.search(r'box_[0-9]+', filename)
	box = box.group()
	box_no = box.replace('box', '')
	box_no = box_no.replace('_', '')
	while len(box_no) < 5:
		box_no = '0' + box_no
	return 'box_' + box_no 


def replace_box_no(filename):
	# pp(filename)
	correct_box_no = pad_box_no(filename)
	bad_box_no = re.search(r'box_[0-9]+', filename)
	bad_box_no = bad_box_no.group()
	filename = filename.replace(bad_box_no, correct_box_no)
	return filename


def pad_folder_no(filename):
	# _634
	folder = re.search(r'fl_[0-9]+[a-zA-Z]?', filename)
	folder = folder.group()
	# pp(folder)
	folder_no = folder.replace('fl', '')
	folder_no = folder_no.replace('_', '')
	if 'a' in folder_no:
		while len(folder_no) < 6:
			folder_no = '0' + folder_no
	else:
		while len(folder_no) < 5:
			folder_no = '0' + folder_no
	return 'fl_' + folder_no 


def replace_folder_no(filename):
	# pp(filename)
	correct_folder_no = pad_folder_no(filename)
	bad_folder_no = re.search(r'fl_[0-9]+[a-zA-Z]?', filename)
	bad_folder_no = bad_folder_no.group()
	# pp(bad_folder_no)
	filename = filename.replace(bad_folder_no, correct_folder_no)
	# pp(filename)
	return filename


def fix_filename(filename):
	pp(filename)
	correct_box_no = replace_box_no(filename)
	correct_folder_no = replace_folder_no(correct_box_no)
	return correct_folder_no


def replace_image_nos(list_of_filenames):
	# pp(list_of_filenames)
	correct_list = []
	count = 1
	for f in list_of_filenames:
		file = re.search(r'fl_[0-9]+', f)
		split = f.split(file.group())
		to_be_replaced = split[-1][1:]

		image_no = str(count)
		while len(image_no) < 6:
			image_no = '0' + image_no

		image_no = image_no + '.tif'
		
		correct_f = f.replace(to_be_replaced, image_no)
		correct_f = fix_filename(correct_f)
		# pp(correct_f)
		count += 1

		# correct_f = fix_filename(correct_f)
		correct_list.append(correct_f)

	return correct_list


if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='')
	parser.add_argument('csv', help='csv of alma data')
	parser.add_argument('outfile', help='csv of alma data')
	args = parser.parse_args()


	filenames = {}
	fns_list = []
	with open(args.csv, encoding='utf-8', errors='ignore') as csv_file:
		reader = csv.DictReader(csv_file)
		for row in reader:
			fns_list.append(row['Old'])
			box_and_folder = re.search(r'box_[0-9]+_fl_[0-9]+[a-zA-Z]?', row['Old']).group()
			if filenames.get(box_and_folder) != None:
				continue
			else:
				filenames[box_and_folder] = []


	for f in fns_list:
		box_and_folder = re.search(r'box_[0-9]+_fl_[0-9]+[a-zA-Z]?', f).group()
		filenames[box_and_folder].append(f)


	rows = []
	for k, v in filenames.items():
		# pp(v)
		corrected_fns = replace_image_nos(v)
		rows.extend(corrected_fns)


	new_rows = []
	for r in rows:
		if re.search(r'fl_[0-9]+[a-zA-Z]+', r) != None:
			a = re.search(r'fl_[0-9]+[a-zA-Z]+', r)
			underscore = a.group() + '_'
			r = r.replace(a.group(), underscore)

		d = {}
		d['correct'] = r
		new_rows.append(d)


	keys = new_rows[0].keys()
	with open(args.outfile, 'w', encoding='utf-8', errors='ignore', newline='') as output:
		w = csv.DictWriter(output, keys)
		w.writeheader()
		w.writerows(new_rows)


	# t = ['Image_Repository\Conroy\midwest_ms_conroy_box_001_fl_001a_001_001.tif','Image_Repository\Conroy\midwest_ms_conroy_box_001_fl_001a_001_002.tif']
	# ts = replace_image_nos(t)

	# rows = []
	# with open(args.csv, encoding='utf-8', errors='ignore') as csv_file:
	# 	reader = csv.DictReader(csv_file)
	# 	for row in reader:
	# 		row['command'] = f'mv -vi {row["Old"]} {row["correct"]}'
	# 		rows.append(row)


	keys = rows[0].keys()
	with open(args.outfile, 'w', encoding='utf-8', errors='ignore', newline='') as output:
		w = csv.DictWriter(output, keys)
		w.writeheader()
		w.writerows(rows)
