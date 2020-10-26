#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse

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
    return list_parents

def getName(node):
    if node['essName'] is not None:
        return node['essName']
    else:
        return "No essName defined."

def getID(node):
    if node['id'] is not None:
        return node['id']
    else:
        return "Error retrieving ID."

def formatOutput(tag,description):
    desc = description.replace('\n', ' ')

    return [tag, ' ( ' + desc + ' )']

def addID(id):
    if id is not None:
        return ' {' + id + '}'
    else:
        return ' {No ID found}'

def addName(name):
    if name is not None:
        return ' [' + name + ']'
    else:
        return ' [No essName found]'

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('--tag', help = "Match node by tag.")
parser.add_argument('--cable', help = "Match node by cableName.")
parser.add_argument('--name', help = "Match node by essName.")
parser.add_argument('--withName', nargs = '?', const = True, default = None, help='Include ESS name in the output.')
parser.add_argument('--id', nargs = '?', const = True, default = None, help='Include ESS ID (ESS-#######) in the output.')
parser.add_argument('--naked', nargs = '?', const = True, default = None, help='Show only the matching breakdown structure tab.')

args = parser.parse_args()
inFile = args.inFile
matchTag = args.tag
matchCable = args.cable
matchName = args.name
naked = args.naked

withName = args.withName
withID = args.id

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)
leadingChar = listBreakdown[0]['tag'][0]

rootNode = listBreakdown[0]['tag']


# Parse the breakdown structure for matchTaging nodes
#Handle special case of '++ESS.A' in LBS
if matchTag is not None:
    if matchTag[:2] == '++':
        matchTag = matchTag.replace('++ESS.','+ESS.')

    if rootNode not in matchTag:
        matchTag = rootNode + '.' + matchTag

    # Allow lazy prescription of matchTag
    # And autofill any missing leading char.
    if leadingChar == '=':
        if matchTag[0] != '=':
            breakdown = 'lbs'
            matchTag = "=" + matchTag
        elif leadingChar == '+':
            if matchTag[0] != '+':
                matchTag = '+' + matchTag
                breakdown = 'fbs'
            else:
                print("Input file is unsupported. Must be 'lbs' or 'fbs' breakdown structure.")
                exit(1) 

    list_parents = getAllParents(matchTag)
    list_matchedParents = list()


matchedNode = ""


for el in listBreakdown:
    noClash = 0
    tagFull = el['tag']
    essName=''
    essID=''
    foundMatches = False
    if matchName is not None:
        if el['essName'] == matchName:
            matchedNode = formatOutput(tagFull, el['description']) 
            break
    if matchCable is not None:
        if el['cableName'] == matchCable:
            matchedNode = formatOutput(tagFull, el['description']) 
            break
    if matchTag is not None:
        if tagFull in list_parents:
            list_matchedParents.append(formatOutput(tagFull, el['description']))
        if tagFull == matchTag:
            matchedNode = formatOutput(tagFull, el['description']) 
            break


if withName:
    matchedNode.append(addName(el['essName']))
if withID:
    matchedNode.append(addID(el['id']))

if len(matchedNode) > 0 and matchTag is None:
    list_parentNodes = list()
    list_parents = getAllParents(matchedNode[0])
    list_matchedParents = list()
    for el in listBreakdown:
        tagFull = el['tag']
        if tagFull in list_parents:
            list_matchedParents.append(tagFull + ' ( ' + el['description'] + ' ) ')
        if len(list_matchedParents) == len(list_parents):
            break

if len(matchedNode) > 0 and len(list_matchedParents) > 0:
    strOut = ''
    if naked is None:
        for el in matchedNode:
            strOut += el
    else:
        strOut = matchedNode[0]
    print(strOut)
    if naked is None:
        print("*** Parent nodes ***")
        for el in list_matchedParents:
            print(el)
else:
    print("No matched node.")
