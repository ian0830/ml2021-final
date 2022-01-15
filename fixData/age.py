def fixAge(header, content):
    indexAge = header.index('Age')
    indexUnder30 = header.index('Under 30')
    indexSenior = header.index('Senior Citizen')

    return header, content