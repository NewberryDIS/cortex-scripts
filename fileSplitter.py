import csv

allData = []

outputDict = {}

with open('./output/allData-211001.csv') as infile:
    allData = csv.reader(infile, delimiter=",")
    header = []
    count = 0
    for row in allData:
        if count == 0: 
            header = row
        if count > 0:
            # print('ok')
            rowObj = {}
            for idx, val in enumerate(row):
                rowObj[header[idx]] = val
            bibid  = rowObj['BIBID']
            # print(bibid)
            if bibid not in outputDict:
                outputDict[bibid] = [rowObj]
            else:
                outputDict[bibid].append(rowObj)
        count += 1
for f in outputDict:
    filename = './output/split/' + f + '.csv' 
    keys = outputDict[f][0].keys()
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(outputDict[f])
    print(filename)