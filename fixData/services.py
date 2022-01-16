def fixMoney(header, content):
    indexTotalDist = header.index('Total Long Distance Charges')
    indexTenure = header.index('Tenure in Months')
    indexAvgDist = header.index('Avg Monthly Long Distance Charges')
    indexTotalRevenue = header.index('Total Revenue')
    indexTotalCharges = header.index('Total Charges')
    indexTotalData = header.index('Total Extra Data Charges')
    indexTotalRefunds = header.index('Total Refunds')
    indexCharges = header.index('Monthly Charge')
    def empty(row, listOfIndex):
        count = 0
        for index in listOfIndex:
            if row[index] == '':
                count+=1
        return count

    for i in range(len(content)):
        row = content[i]
        fixSomething = True
        while fixSomething:
            fixSomething = False
            if empty(row, [indexTotalDist, indexTenure, indexAvgDist]) == 1:
                totalDist, tenure, avgDist = row[indexTotalDist], row[indexTenure], row[indexAvgDist]
                fixSomething = True
                if totalDist == '':
                    row[indexTotalDist] = str(float(tenure) * float(avgDist))
                if tenure == '':
                    if float(avgDist) == 0:
                        fixSomething = False
                    else: row[indexTenure] = str(float(totalDist) / float(avgDist))
                if avgDist == '':
                    if float(tenure) == 0:
                        fixSomething = False
                    else: row[indexAvgDist] = str(float(totalDist) / float(tenure))
            if empty(row, [indexTotalRevenue, indexTotalCharges, indexTotalData, indexTotalDist, indexTotalRefunds]) == 1:
                revenue, charges, data, dist, refunds = row[indexTotalRevenue], row[indexTotalCharges], row[indexTotalData], row[indexTotalDist], row[indexTotalRefunds]
                fixSomething = True
                if revenue == '':
                    row[indexTotalRevenue] = str(float(charges) + float(data) + float(dist) - float(refunds))
                if charges == '':
                    row[indexTotalCharges] = str(float(revenue) - float(data) - float(dist) + float(refunds))
                if data == '':
                    row[indexTotalData] = str(float(revenue) - float(charges) - float(dist) + float(refunds))
                if dist == '':
                    row[indexTotalDist] = str(float(revenue) - float(charges) - float(data) + float(refunds))
                if refunds == '':
                    row[indexTotalRefunds] = str(float(charges) + float(data) + float(dist) -float(revenue))
            if empty(row, [indexTotalCharges, indexTenure, indexCharges]) == 1:
                total, tenure, monthly = row[indexTotalCharges], row[indexTenure], row[indexCharges]
                fixSomething = True
                if total == '':
                    row[indexTotalCharges] = str(float(tenure) * float(monthly))
                if tenure == '':
                    if float(monthly) == 0:
                        fixSomething = False
                    else: row[indexTenure] = str(float(total) / float(monthly))
                if monthly == '':
                    if float(tenure) == 0:
                        fixSomething = False
                    else: row[indexCharges] = str(float(total) / float(tenure))
            else: break
        content[i] = row
    return header, content