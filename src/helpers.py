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
