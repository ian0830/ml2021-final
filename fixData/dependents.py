import numpy as np


def fixDependents(header, content):
    indexDep = header.index('Dependents')
    indexNumOfDep = header.index('Number of Dependents')
    medianHave = np.median(np.array([float(
        row[indexNumOfDep]) for row in content if row[indexDep] == 'Yes' and row[indexNumOfDep] != '']))
    median = np.median(np.array([float(row[indexNumOfDep] if row[indexNumOfDep] != '' else (
        medianHave)) for row in content if row[indexNumOfDep] != '' or row[indexDep] == 'Yes']))
    print(medianHave, median)
    for i in range(len(content)):
        row = content[i]
        Dep = row[indexDep]
        NumOfDup = row[indexNumOfDep]
        if Dep != '' and NumOfDup != '':
            continue
        if Dep != '':
            if Dep == 'Yes':
                if NumOfDup == '':
                    row[indexNumOfDep] = medianHave
            if Dep == 'No':
                if NumOfDup == '':
                    row[indexNumOfDep] = '0'

        if NumOfDup != '':
            if float(NumOfDup) > 0:
                if Dep == '':
                    row[indexDep] = 'Yes'
            if float(NumOfDup) == 0:
                if Dep == '':
                    row[indexDep] = 'No'

        if Dep == '' and NumOfDup == '':
            row[indexDep] = 'No' if median == 0 else 'Yes'
            row[indexNumOfDep] = median

        content[i] = row
    return header, content
