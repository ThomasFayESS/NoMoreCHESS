#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('findMatch', help = "Match this node.")
parser.add_argument('--withNames', nargs = '?', const = True, default = None, help='Include ESS name in the output.')
parser.add_argument('--id', nargs = '?', const = True, default = None, help='Include ESS ID (ESS-#######) in the output.')


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

def dropNewLines(str):
    return str.replace('\n', ' ')

args = parser.parse_args()
inFile = args.inFile
findMatch = args.findMatch
withNames = args.withNames
withID = args.id

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)
leadingChar = listBreakdown[0]['tag'][0]

rootNode = listBreakdown[0]['tag']


# Parse the breakdown structure for findMatching nodes
#Handle special case of '++ESS.A' in LBS
if findMatch[:2] == '++':
    findMatch = findMatch.replace('++ESS.','+ESS.')

if rootNode not in findMatch:
    findMatch = rootNode + '.' + findMatch

list_parentNodes = list()
list_parents = getAllParents(findMatch)

# Allow lazy prescription of findMatch
# And autofill any missing leading char.
if leadingChar == '=':
    if findMatch[0] != '=':
        breakdown = 'lbs'
        findMatch = "=" + findMatch
    elif leadingChar == '+':
        if findMatch[0] != '+':
            findMatch = '+' + findMatch
            breakdown = 'fbs'
        else:
            print("Input file is unsupported. Must be 'lbs' or 'fbs' breakdown structure.")
            exit(1) 


matchedNode = ""
list_matchedParents = list()


for el in listBreakdown:
    noClash = 0
    tagFull = el['tag']
    essName=''
    essID=''
    foundMatches = False
    if tagFull in list_parents:
        list_matchedParents.append([tagFull, dropNewLines(el['description']),"", ""])
    if tagFull == findMatch:
        matchedNode = el['tag'] + ' ( ' + dropNewLines(el['description']) + ' )'
        if withNames:
            matchedNode += '[' + essName + ']'
        if withID:
            matchedNode += '{' + essID + '}'
        break


if len(matchedNode) > 0 and len(list_matchedParents) > 0:
    print(matchedNode)
    print("*** Parent nodes ***")
    for el in list_matchedParents:
        print(el[0] + ' ( ' + el[1] + ' )')
else:
    print("No matched node.")
