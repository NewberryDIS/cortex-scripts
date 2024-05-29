from pprint import pprint as pp
import os



if __name__ == '__main__':

	# find IR folders with bib- prefix
	# add BibID prefix from the first file to all files
	# change folder prefix from bib- to ur- (upload ready)

	directory = '.' # Image_Repository
	# directory = 'image_repository/' ## Test
	for folder in os.listdir(directory):
		# pp(folder)
		folder_path = os.path.join(directory, folder)
		if os.path.isdir(folder_path) == True:
			if 'bib' in folder:
				new_folder = folder.replace('bib', 'ur')
				# pp(new_folder)
				first_file = os.listdir(folder_path)[0]
				# pp(first_file)
				bibid = first_file.split('_')[0]
				# pp(bibid)
				for file in os.listdir(folder_path):
					# pp(file)
					if bibid not in file:
						# pp(file)
						new_file = bibid + '_' + file 
						# pp(new_file)
						os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_file))

				os.rename(os.path.join(directory, folder), os.path.join(directory, new_folder))

