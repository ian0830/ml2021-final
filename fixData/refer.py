def fixRefer(header, content):
    indexRefFriend =  header.index('Referred a Friend')
    indexNumOfRef = header.index('Number of Referrals')
    
    return header, content