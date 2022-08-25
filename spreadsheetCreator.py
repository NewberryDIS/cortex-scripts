import csv

# input file should be a list of paths
file1 = open('monroeSports.txt', 'r')
monroeSports = file1.readlines()

prevPath = [ 1,2,3,4 ]
headerList = [
    "BIBID",
    "FILENAME",
    "TITLE",
    "CATALOG_LINK",
    "CONTRIBUTING_INSTITUTION",
    "OA_POLICY",
    "DISCLAIMER_STMT",
    "DCMIType",
    "CREATOR",
    "PUBLISHER_ORIGINAL",
    "CALL_NUMBER",
    "FORMAT_EXTENT",
    "DESCRIPTION",
    "LANGUAGE",
    "SUBJECTS",
    "PLACE",
    "FORMAT",
    "BIOGRAPHICAL/HISTORICAL NOTE",
    "SUMMARY",
    "DATE_DISPLAY",
    "DATE_SORT",
    "STANDARDIZED_RIGHTS",
    "ARCHIVAL_COLLECTION",
    "DATE_DIGITAL",
    "ACCESS_STMT",
    "TITLE_ALTERNATIVE",
    "CONTRIBUTOR",
    "TRANSCRIPTION",
    "CITATION",
    "IN_COPYRIGHT"
]
dataList = [
    "",
    "",
    "John I. Monroe collection of sports postcards, 1902-1931",
    "",
    "Newberry Library",
    "The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to <a href='https://www.newberry.org/rights-and-reproductions' target='_blank'>these terms and conditions</a>",
    "All materials in the Newberry Library’s collections have research value and reflect the society in which they were produced. They contain language and imagery that are offensive because of content relating to ability, gender, race, religion, sexuality/sexual orientation, and other categories. <a href='https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf' target='_blank'>More information</a>",
    "Still image",
    "Monroe, John I.",
    "",
    "Modern MS Monroe Sports",
    "",
    "Note: This collection-level data is temporary until postcard-level cataloging can be completed.",
    "English",
    "Sports",
    "",
    "Postcards",
    "",
    "",
    "1902-1931",
    "1902/1931",
    "Copyright Not Evaluated",
    "John I. Monroe collection of sports postcards",
    "",
    "",
    "",
    "",
    "",
    "",
] 

# create enpty spreadsheets with correct header
for line in monroeSports:
    fullPath = line.split("/")

    # popping off the filename from the array so we can concatenate it to generate the file in the correct place
    filename = fullPath.pop(-1)
    ssFileName = "/".join(fullPath) + '/Central_' + fullPath[-1] + ".csv"
    try: 
        # create new file
        ssFile = open(ssFileName, "x")
        ssFile.close()
        # write header into file
        ssFile = open(ssFileName, "w")
        writer = csv.writer(ssFile)
        writer.writerow(headerList)
        # gotta close file both times or weird things happen, also best practices etc
        ssFile.close()
    # if the file exists the script will fail so we use a try/except block
    except: 
        print(ssFileName + ": file already exists, skipping...")

# fill spreadsheets with data + filename
for line in monroeSports:
    fullPath = line.split("/")
    filename = fullPath.pop(-1).strip()
    # insert filename at position 2 in the data list; note we're modifying the original list, not creating a new one
    dataList[1] = filename
    # open the file according to its terminal folder (second-to-last element in path list)
    ssFileName = "/".join(fullPath) + '/Central_' + fullPath[-1] + ".csv"
    # opening the file in "append" mode so we don't overwrite the header or data already pushed into it
    appendFile = open(ssFileName, "a", newline="\n")
    writer = csv.writer(appendFile)
    writer.writerow(dataList)
    appendFile.close()

file1.close()
