import numpy as np

def fixRefer(header, content):
    indexRefFriend =  header.index('Referred a Friend')
    indexNumOfRef = header.index('Number of Referrals')
    medianHave = np.median(np.array([float(
        row[indexNumOfRef]) for row in content if row[indexRefFriend] == 'Yes' and row[indexNumOfRef] != '']))
    median = np.median(np.array([float(row[indexNumOfRef] if row[indexNumOfRef] != '' else (
        medianHave)) for row in content if row[indexNumOfRef] != '' or row[indexRefFriend] == 'Yes']))
    for i in range(len(content)):
        row = content[i]
        RefFriend = row[indexRefFriend]
        NumOfRef = row[indexNumOfRef]
        if RefFriend != '' and NumOfRef != '':
            continue
        if RefFriend != '':
            if RefFriend == 'Yes':
                if NumOfRef == '':
                    row[indexNumOfRef] = medianHave
            if RefFriend == 'No':
                if NumOfRef == '':
                    row[indexNumOfRef] = '0'

        if NumOfRef != '':
            if float(NumOfRef) > 0:
                if RefFriend == '':
                    row[indexRefFriend] = 'Yes'
            if float(NumOfRef) == 0:
                if RefFriend == '':
                    row[indexRefFriend] = 'No'

        if RefFriend == '' and NumOfRef == '':
            row[indexRefFriend] = 'No' if median == 0 else 'Yes'
            row[indexNumOfRef] = median

        content[i] = row
    return header, content