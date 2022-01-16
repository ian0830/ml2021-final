import numpy as np


def fixDependents(header, content):
    indexDep = header.index('Dependents')
    indexNumOfDep = header.index('Number of Dependents')
    medianHave = np.median(np.array([float(
        row[indexNumOfDep]) for row in content if row[indexDep] == 'Yes' and row[indexNumOfDep] != '']))
    median = np.median(np.array([float(row[indexNumOfDep] if row[indexNumOfDep] != '' else (
        medianHave)) for row in content if row[indexNumOfDep] != '' or row[indexDep] == 'Yes']))
    for i in range(len(content)):
        row = content[i]
        Dep = row[indexDep]
        NumOfDep = row[indexNumOfDep]
        if Dep != '' and NumOfDep != '':
            continue
        if Dep != '':
            if Dep == 'Yes':
                if NumOfDep == '':
                    row[indexNumOfDep] = medianHave
            if Dep == 'No':
                if NumOfDep == '':
                    row[indexNumOfDep] = '0'

        if NumOfDep != '':
            if float(NumOfDep) > 0:
                if Dep == '':
                    row[indexDep] = 'Yes'
            if float(NumOfDep) == 0:
                if Dep == '':
                    row[indexDep] = 'No'

        if Dep == '' and NumOfDep == '':
            row[indexDep] = 'No' if median == 0 else 'Yes'
            row[indexNumOfDep] = median

        content[i] = row
    return header, content
