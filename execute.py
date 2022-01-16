#!/usr/bin/python3
from csvfiledata import *
from fixData import *
from fixData.age import fixAge
from fixData.dependents import fixDependents
from fixData.refer import fixRefer
from fixData.services import fixMoney

files = [
    'demographics.csv', 'location.csv', 'satisfaction.csv', 'services.csv', 'status.csv']

if __name__ == '__main__':
    # merging to a big spreadsheet
    resultHeader, resultContent= [],[[]]
    for file in files:
        header, content = get_file(file)
        if (len(resultHeader) == 0):
            resultHeader, resultContent = header, content
        else: 
            resultHeader, resultContent = merge_file(resultContent, content, resultHeader, header)
    
    # Extract sample_submission IDs and sorted from the big spreadsheet
    # sample_submission: Test_IDs
    # status: Train_IDs
    header, content = get_file('sample_submission.csv')
    ids = [row[0] for row in content]
    sortedContent = []
    for _id in ids:
        sortedContent.append([row[0:] for row in resultContent if row[0] == _id][0])
    resultContent = sortedContent

    resultHeader, resultContent = fixAge(resultHeader, resultContent)
    resultHeader, resultContent = fixDependents(resultHeader, resultContent)
    resultHeader, resultContent = fixRefer(resultHeader, resultContent)



    # write_file('before.csv', resultHeader[1:],[row[1:] for row in resultContent])

    resultHeader, resultContent = fixMoney(resultHeader, resultContent)

    # write_file('after.csv', resultHeader[1:],[row[1:] for row in resultContent])



    statusIndex = resultHeader.index('Churn Category')
    resultHeader = [resultHeader[0]] + [resultHeader[statusIndex]] + resultHeader[1:statusIndex] + resultHeader[statusIndex+1:]
    for i in range(len(resultContent)):
        resultContent[i] = [resultContent[i][0]] + [resultContent[i][statusIndex]] + resultContent[i][1:statusIndex] + resultContent[i][statusIndex+1:]

    # append population by zip code to each row
    popHeader, popContent = get_file('population.csv')
    appendHeader = popHeader[2]
    appendContent = []
    transformation = {}
    for row in popContent:
        transformation[float(row[1])] = row[2]
    index = resultHeader.index("Zip Code")
    for row in resultContent:
        if row[index] != '' and float(row[index]) > 0:
            appendContent.append([transformation[float(row[index])]])
        else:
            appendContent.append([''])
    
    resultHeader = resultHeader[0: index] + [appendHeader] + resultHeader[index:]
    for i in range(len(resultContent)): resultContent[i] = resultContent[i][0: index] + appendContent[i]+ resultContent[i][index:]

    # exclude irrelevant value (meaningless)
    exclude = ['Count', 'Country', 'State', 'City', 'Zip Code','Lat Long', 'Quarter']
    for target in exclude:
        index = resultHeader.index(target)
        resultHeader = resultHeader[0: index] + resultHeader[index+1:]
        for i in range(len(resultContent)): resultContent[i] = resultContent[i][0: index] + resultContent[i][index+1:]

    # insert value-column for categorical values
    categorical = ['Gender', 'Under 30', 'Senior Citizen', 'Married', 'Dependents','Referred a Friend', 'Offer', 'Phone Service', 'Multiple Lines', 'Internet Service', 'Internet Type',  'Online Security', 'Online Backup', 'Device Protection Plan', 'Premium Tech Support', 'Streaming TV', 'Streaming Movies', 'Streaming Music', 'Unlimited Data', 'Contract', 'Paperless Billing', 'Payment Method']
    numerical = [header for header in resultHeader[2:] if not (header in categorical)]
    for feature in categorical:
        index = resultHeader.index(feature)
        values = set()
        for row in resultContent:
            if row[index] != '': values.add(row[index])
        values = list(values)
        appendHeader = [feature + '-' + value for value in values]
        appendContent = []
        for row in resultContent:
            appendRow = [0]*len(appendHeader)
            if not (row[index] == ''):
                appendRow[appendHeader.index(feature + '-' + row[index])] = 1
            appendContent.append(appendRow)
        resultHeader = resultHeader[0: index] + resultHeader[index+1:] + appendHeader
        for i in range(len(resultContent)): resultContent[i] = resultContent[i][0: index] + resultContent[i][index+1:] + appendContent[i]

    status = {
        'No Churn': 0,
        'Competitor': 1,
        'Dissatisfaction': 2,
        'Attitude': 3,
        'Price': 4,
        'Other': 5,
        '': 6
    }
    for i in range(len(resultContent)):
        resultContent[i][1] = status[resultContent[i][1]]

    # 選擇要輸出的欄位
    # selected = ["Customer ID", "Churn Category", "Satisfaction Score"]
    # selectedIndex = [i for i in range(len(resultHeader)) for col in selected if resultHeader[i].startswith(col)] #startswith
    # resultHeader = [resultHeader[i] for i in range(len(resultHeader)) if i in selectedIndex]
    # for i in range(len(resultContent)): resultContent[i] = [resultContent[i][j] for j in range(len(resultContent[i])) if j in selectedIndex]

    # print(resultHeader)
    # print(resultContent[0][0:4])
    # output0 = sample([row for row in resultContent if row[1] == 0],116)
    # output1 = sample([row for row in resultContent if row[1] == 1],116)
    # output2 = sample([row for row in resultContent if row[1] == 2],116)
    # output3 = sample([row for row in resultContent if row[1] == 3],116)
    # output4 = sample([row for row in resultContent if row[1] == 4],116)
    # output5 = sample([row for row in resultContent if row[1] == 5],116)
    # resultContent = output0 + output1 + output2 + output3 + output4 + output5
    # 輸出到result.csv
    write_file('adaBoost/result_test.csv', resultHeader[1:],[row[1:] for row in resultContent])
