'''
Breakdown structure nodes usually make little sense on their own.
Beneficial to append parent node information when displaying a node.
'''
def getAllParents(node):
    currentNode = node
    list_parents = list()
    nLevels = currentNode.count('.')
    while nLevels > 0:
        temp = currentNode.split('.')
        for i in range (0, nLevels):
            if i == 0:
                currentNode = temp[0]
            else:
                currentNode += '.' + temp[i]
        nLevels = currentNode.count('.')
        list_parents.append(currentNode) 
    list_parents.sort()
    return list_parents

'''
Get commonRoot node if filter pattern has one
'''
def getRoot(str):
    strOut=str[0]
    for char in str[1:]:
        if char.isalnum() or char == '.':
            strOut += char
        else:
            break
    cntNodes = strOut.count('.')
    if cntNodes > 0:
        temp = strOut.split('.')
    else:
        return None
    strOut = temp[0]
    for el in temp[1:-1]:
        strOut += '.' + el
    if str[-1] == '$':
        strOut += '.' + temp[-1]
    return strOut

wgetArgs=['wget', '--header', 'Host: chess.esss.lu.se',
'--user-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
'--header', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'--header', 'Accept-Language: en-GB,en;q=0.5',
'--referer', 'https://chess.esss.lu.se/enovia/ess/webdav/essWebdavIntegrationFrame.jsp',
'--header', 'Cookie: JSESSIONID=365C3A9A6C158112C24706F918A965C0.instance_E1; RBACCookie=YTgzN2E0MjYtOTZkMi0zZDM5LTllODEtMTgxMmUwNTIzOGFj; _ga=GA1.2.363358576.1601474201; afs=41979825-ce7d-422e-a341-68982f3d4d60; _gid=GA1.2.1173947252.1605003065; swymlang=en',
'--header', 'Upgrade-Insecure-Requests: 1',
'https://chess.esss.lu.se/enovia/tvc-action/essDocumentDownload?versionObjectId={{ LINK_ID }}&inline=false',
'--output-document', '../docs/{{ FILENAME }}']
