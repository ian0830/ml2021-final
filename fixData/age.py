import numpy as np


def fixAge(header, content):
    indexAge = header.index('Age')
    median = np.median(np.array([float(
        row[indexAge]) for row in content if row[indexAge] != '' and 30 > float(row[indexAge])]))
    medianUnder30 = np.median(np.array(
        [float(row[indexAge]) for row in content if row[indexAge] != '' and 30 > float(row[indexAge])]))
    medianOver30 = np.median(np.array(
        [float(row[indexAge]) for row in content if row[indexAge] != '' and 30 >= float(row[indexAge])]))
    median30_65 = np.median(np.array(
        [float(row[indexAge]) for row in content if row[indexAge] != '' and 30 <= float(row[indexAge]) < 65]))
    medianUnder65 = np.median(np.array(
        [float(row[indexAge]) for row in content if row[indexAge] != '' and 65 < float(row[indexAge])]))
    medianOver65 = np.median(np.array(
        [float(row[indexAge]) for row in content if row[indexAge] != '' and 65 <= float(row[indexAge])]))
    indexUnder30 = header.index('Under 30')
    indexSenior = header.index('Senior Citizen')
    for i in range(len(content)):
        row = content[i]
        Age, Under30, Senior = row[indexAge], row[indexUnder30], row[indexSenior]
        if (Age != '' and Under30 != '' and Senior != ''):
            continue
        if Age != '':
            # 有填確切年齡
            age = float(Age)
            if age < 30:
                row[indexUnder30], row[indexSenior] = 'Yes', 'No'
            elif age >= 65:
                row[indexUnder30], row[indexSenior] = 'No', 'Yes'
            else:
                row[indexUnder30], row[indexSenior] = 'No', 'No'

        if Under30 != '':
            if Under30 == 'Yes':
                if Senior == '':
                    row[indexSenior] = Senior = 'No'
                if Age == '':
                    if Senior == 'No':
                        row[indexAge] = medianUnder30
                    if Senior == 'Yes':
                        row[indexAge] = median
            if Under30 == 'No':
                if Senior == '':
                    row[indexSenior] = Senior = 'Yes' if medianOver30 >= 65 else 'No'
                if Age == '':
                    if Senior == 'Yes':
                        row[indexAge] = medianOver65
                    if Senior == 'No':
                        row[indexAge] = median30_65

        if Senior != '':
            if Senior == 'Yes':
                if Under30 == '':
                    row[indexUnder30] = Under30 = 'No'
                if Age == '':
                    if Under30 == 'No':
                        row[indexAge] = medianOver65
                    if Under30 == 'Yes':
                        row[indexAge] = median
            if Senior == 'No':
                if Under30 == '':
                    row[indexUnder30] = Under30 = 'Yes' if medianUnder65 < 30 else 'No'
                if Age == '':
                    if Under30 == 'Yes':
                        row[indexAge] = medianUnder30
                    if Under30 == 'No':
                        row[indexAge] = median30_65

        if Age == '' and Under30 == '' and Senior == '':
            row[indexAge] = median
            row[indexUnder30] = 'Yes' if median < 30 else 'No'
            row[indexSenior] = 'Yes' if median >= 65 else 'No'

        content[i] = row
    return header, content
