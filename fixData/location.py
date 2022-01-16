import csv
from uszipcode import SearchEngine

def get_file(fileName):
    # return (header, content)
    result = []
    with open(fileName, encoding='utf-8', newline='') as csvfile:
        rows = csv.reader(csvfile)
        header = next(rows)
        for row in rows:
            result.append(row)
        csvfile.close()
    return header, result

def write_file(fileName, datafileheader, datafile):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(datafileheader)
        for filedata in datafile:
            writer.writerow(filedata)

def fixLocation(header, content):
    # Extract category index
    index = ['City', 'Zip Code', 'Lat Long', 'Latitude', 'Longitude']
    indexList = [header.index(item) for item in index]
    # process: create dict, compare, get result
    engine = SearchEngine()
    # merge 'Lat Long', 'Latitude', 'Longitude'
    targetIndexList = indexList[2:]
    latDict = {}
    for i in range(len(content)):
        if (content[i][targetIndexList[0]] != '') and (content[i][targetIndexList[1]] == '' or content[i][targetIndexList[2]] == ''):
            temp = content[i][targetIndexList[0]].split(', ')
            if content[i][targetIndexList[1]] == '': content[i][targetIndexList[1]] = temp[0]
            if content[i][targetIndexList[2]] == '': content[i][targetIndexList[2]] = temp[1]
        if content[i][targetIndexList[1]] == '' and latDict.get(content[i][targetIndexList[2]]) != None:
            content[i][targetIndexList[1]] = latDict[content[i][targetIndexList[2]]]
        if content[i][targetIndexList[2]] == '' and latDict.get(content[i][targetIndexList[1]]) != None:
            content[i][targetIndexList[2]] = latDict[content[i][targetIndexList[1]]]
        if (content[i][targetIndexList[0]] == '') and ((content[i][targetIndexList[1]] != '' and latDict.get(content[i][targetIndexList[1]]) != None) or (content[i][targetIndexList[2]] != '' and latDict.get(content[i][targetIndexList[2]]) != None)):
            temp = content[i][targetIndexList[1]]+latDict[content[i][targetIndexList[1]]] if content[i][targetIndexList[1]] != '' else latDict[content[i][targetIndexList[2]]]+content[i][targetIndexList[2]]
            content[i][targetIndexList[0]] = content[i][targetIndexList[1]] + ", " + content[i][targetIndexList[2]]
        if content[i][targetIndexList[0]] == '' and content[i][targetIndexList[1]] != '' and content[i][targetIndexList[2]] != '':
            content[i][targetIndexList[0]] = content[i][targetIndexList[1]] + ", " + content[i][targetIndexList[2]]
        if content[i][targetIndexList[1]] != '' and content[i][targetIndexList[2]] != '':
            latDict[content[i][targetIndexList[1]]] = content[i][targetIndexList[2]]
            latDict[content[i][targetIndexList[2]]] = content[i][targetIndexList[1]]
    # again
    for i in range(len(content)):
        if (content[i][targetIndexList[0]] != '') and (content[i][targetIndexList[1]] == '' or content[i][targetIndexList[2]] == ''):
            temp = content[i][targetIndexList[0]].split(', ')
            if content[i][targetIndexList[1]] == '': content[i][targetIndexList[1]] = temp[0]
            if content[i][targetIndexList[2]] == '': content[i][targetIndexList[2]] = temp[1]
        if content[i][targetIndexList[1]] == '' and latDict.get(content[i][targetIndexList[2]]) != None:
            content[i][targetIndexList[1]] = latDict[content[i][targetIndexList[2]]]
        if content[i][targetIndexList[2]] == '' and latDict.get(content[i][targetIndexList[1]]) != None:
            content[i][targetIndexList[2]] = latDict[content[i][targetIndexList[1]]]
        if (content[i][targetIndexList[0]] == '') and ((content[i][targetIndexList[1]] != '' and latDict.get(content[i][targetIndexList[1]]) != None) or (content[i][targetIndexList[2]] != '' and latDict.get(content[i][targetIndexList[2]]) != None)):
            temp = content[i][targetIndexList[1]]+latDict[content[i][targetIndexList[1]]] if content[i][targetIndexList[1]] != '' else latDict[content[i][targetIndexList[2]]]+content[i][targetIndexList[2]]
            content[i][targetIndexList[0]] = content[i][targetIndexList[1]] + ", " + content[i][targetIndexList[2]]
        if content[i][targetIndexList[0]] == '' and content[i][targetIndexList[1]] != '' and content[i][targetIndexList[2]] != '':
            content[i][targetIndexList[0]] = content[i][targetIndexList[1]] + ", " + content[i][targetIndexList[2]]
        if content[i][targetIndexList[1]] != '' and content[i][targetIndexList[2]] != '':
            latDict[content[i][targetIndexList[1]]] = content[i][targetIndexList[2]]
            latDict[content[i][targetIndexList[2]]] = content[i][targetIndexList[1]]
        
    # merge 'City', 'Zip Code'
    targetIndexList = indexList[:2]
    targetDict = {}
    for i in range(len(content)):
        if content[i][targetIndexList[0]] != '' and content[i][targetIndexList[1]] != '':
            targetDict[content[i][targetIndexList[0]]] = content[i][targetIndexList[1]]
            targetDict[content[i][targetIndexList[1]]] = content[i][targetIndexList[0]]
    for i in range(len(content)):
        if content[i][targetIndexList[0]] == '' and content[i][targetIndexList[1]] != '' and targetDict.get(content[i][targetIndexList[1]]) != None:
            content[i][targetIndexList[0]] = targetDict[content[i][targetIndexList[1]]]
        elif content[i][targetIndexList[1]] == '' and content[i][targetIndexList[0]] != '' and targetDict.get(content[i][targetIndexList[0]]) != None:
            content[i][targetIndexList[1]] = targetDict[content[i][targetIndexList[0]]]
    
    return header, content

if __name__ == '__main__':
    fileName = 'test_file.csv'
    fileHeader, fileData = get_file(fileName)
    resultHeader, resultData = fixLocation(fileHeader, fileData)
    write_file('try.csv', resultHeader, resultData)