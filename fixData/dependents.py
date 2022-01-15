def fixDependents(header,content):
    indexDep = header.index('Dependents')
    indexNumOfDep = header.index('Number of Dependents')
    return header, content