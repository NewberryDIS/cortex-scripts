import os
import csv



directory = '.'

filenames = []
for folder in os.listdir(directory):
	folder_path = os.path.join(directory, folder):
	for f in os.listdir(folder_path):
		if f == 'TIFF':
			f_path = os.path.join(folder, f)
			for file in f_path:
				pp(file)
				filenames.append(file)

