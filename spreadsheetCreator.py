import csv

# input file should be a list of paths
filePathsTextFile = open('monroeSports.txt', 'r')
filePathsFullList = filePathsTextFile.readlines()

prevPath = [ 1,2,3,4 ]

headerList = []
dataList = []

# input csv should be a sample data file with header and one row of sample data; any other rows will be ignored
with open ('Central_MonroeJ_Sports.csv', 'r') as csvfile: 
    sampleData = csv.reader(csvfile)
    headerList = next(sampleData)
    for idx, row in enumerate(sampleData):
        if idx == 0:
            dataList = row
        else: 
            break

# create new spreadsheets with header

for line in filePathsFullList:
    fullPath = line.split("/")

    # popping off the filename from the array so we can concatenate it to generate the file in the correct place
    filename = fullPath.pop(-1)
    ssFileName = "/".join(fullPath) + '/Central_' + fullPath[-1] + ".csv"

    # if the file exists the script will fail so we use a try/except block
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
    except: 
        print(ssFileName + ": file already exists, skipping...")

# fill spreadsheets with data + filename
for line in filePathsFullList:
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

filePathsTextFile.close()
