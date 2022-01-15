import csv

"""
get_file(fileName)
get_file_header(fileName)
get_file_name()
get_file_with_row_target(fileName, row_target)
get_file_with_column_target(fileName, column_target)
print_cvs_file(datafile)
"""

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

def merge_file(data1, data2, data1_header, data2_header):
    header = []
    headerDict = {}
    header_counter = 0
    # deal with headers
    for item in data1_header:
        header.append(item)
        headerDict[item] = header_counter
        header_counter = header_counter + 1
    for item in data2_header:
        if not(item in header):
            header.append(item)
            headerDict[item] = header_counter
            header_counter = header_counter + 1
    # data
    result = []
    resultDict = {}
    result_counter = 0
    for i in range(len(data1)):
        resultDict[data1[i][0]] = result_counter
        result_counter = result_counter + 1
        result.append(['' for i in range(len(header))])
        for j in range(len(data1[i])):
            result[resultDict[data1[i][0]]][headerDict[data1_header[j]]] = data1[i][j]
    for i in range(len(data2)):
        if resultDict.get(data2[i][0]) == None:
            resultDict[data2[i][0]] = result_counter
            result_counter = result_counter + 1
            result.append(['' for i in range(len(header))])
        for j in range(len(data2[i])):
            result[resultDict[data2[i][0]]][headerDict[data2_header[j]]] = data2[i][j]
    return  header,result

# def merge_population(data1, data1_header):
#     populationDict = {}
#     populationHeader, populationData = get_file('population.csv')
#     for i in range(len(populationData)): populationDict[populationData[i][1]] = i
#     data1_header.extend(populationHeader[::2])
#     insert = data1_header.index(populationHeader[1])
#     for i in range(len(data1)):
#         if populationDict.get(data1[i][insert]) != None: data1[i].extend(populationData[populationDict[data1[i][insert]]][::2])
#         else: data1[i].extend([-1, -1])
#     return data1, data1_header

def write_file(fileName, datafileheader, datafile):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(datafileheader)
        for filedata in datafile:
            writer.writerow(filedata)

def print_csvfile(datafile):
    print(*datafile, sep='\n')

if __name__ == '__main__':
    # demo
    # data = Data()
    # datafileName = get_file_name()
    # data.print_csvfile(data.get_file(datafileName[0]))
    print_csvfile(get_file('demographics.csv'))
    # print(len(data.get_file('merge.csv')))