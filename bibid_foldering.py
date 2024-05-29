import os
import re

directory = os.getcwd()
print(directory)
# for filename in os.listdir(directory):
#     if os.path.isfile(os.path.join(directory, filename)):
#         match = re.search(r'^(\d+)', filename)
#         if match:
#             foldername = match.group(1)
#             folderpath = os.path.join(directory, foldername)
#             if not os.path.exists(folderpath):
#                 os.mkdir(folderpath)
#             filepath = os.path.join(directory, filename)
#             os.rename(filepath, os.path.join(folderpath, filename))