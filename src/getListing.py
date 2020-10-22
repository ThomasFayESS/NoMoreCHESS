#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse
import fnmatch
import re

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('--top', help = 'Defines the top node to take listing from. Can be single string or comma delimited list of strings e.g. \'A01,A02,A03\'. Specify absolute node or relative to global root note. Leading \'=\' and \'+\' characters for the relevant breakdown structure are optional.')
parser.add_argument('--match', help = "Allows specification of top node(s) by wildcard. For example '*E??.E01.K01'.")
parser.add_argument('--exclude', help ='Specifies the nodes to be exlucded. Can be a single node IDs or a comma seperated list. For example --exclude K for single node and --example K,KF,WG for a listing.')
parser.add_argument('--levels', type=int, help='Number of levels to show results for. Default is 1')
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
top = args.top
match = args.match
exclude = args.exclude
levels = args.levels
withNames = args.withNames
withID = args.id


# For formatting the matched nodes
midBranch = "├── "
endBranch = "└── "


if exclude is None:
    exclude="ZZZZ"

if levels is None:
    levels = 1
elif levels < 1:
    levels = 50

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)
leadingChar = listBreakdown[0]['tag'][0]

list_exclude = list()
temp = exclude.split(',')
if len(temp) == 1 and not temp[0].isalpha():
    list_exclude.append("ZZZZ")
elif len(temp) == 1 and temp[0].isalpha():
    list_exclude.append(temp[0])
else:
    list_exclude=list(temp)

rootNode = listBreakdown[0]['tag']

list_top = list()
if top is None:
    top = rootNode

temp = top.split(',')
if len(temp) == 1:
    list_top.append(temp[0])
else:
    list_top=list(temp)

#Support pattern matching for top node
if match is not None:
    regex = fnmatch.translate(match)
    list_top.clear()
    for el in listBreakdown:
        if re.search(regex, el['tag']) is not None:
            list_top.append(el['tag'])
    if len(list_top) == 0:
        print("No nodes match pattern: " + match)


#list_matchedNodes = [tag, description, essName, essID]
list_matchedNodes = list()

# Parse the breakdown structure for matching nodes
for top in list_top:
    #Handle special case of '++ESS.A' in LBS
    if top[:2] == '++':
        top = top.replace('++ESS.','+ESS.')

    if rootNode not in top:
        top = rootNode + '.' + top
    list_parentNodes = list()
    list_parents = getAllParents(top)

    # Allow lazy prescription of top
    # And autofill any missing leading or trailing char.
    if not top.endswith("."):
        top=top + "."
    if leadingChar == '=':
        if top[0] != '=':
            breakdown = 'lbs'
            top = "=" + top
        elif leadingChar == '+':
            if top[0] != '+':
                top = '+' + top
                breakdown = 'fbs'
            else:
                print("Input file is unsupported. Must be 'lbs' or 'fbs' breakdown structure.")
                exit(1) 
    for el in listBreakdown:
        noClash = 0
        tagFull = el['tag']
        essName=''
        essID=''
        foundMatches = False
        if tagFull == top[:-1]:
            if withNames:
                essName = getName(el)
            if withID:
                essID = getID(el)
            list_matchedNodes.append([el['tag'],dropNewLines(el['description']),"",""])
        if tagFull in list_parents:
            if withNames:
                essName = getName(el)
            if withID:
                essID = getID(el)
            list_matchedNodes.append([el['tag'],dropNewLines(el['description']),"", ""])
        tag = tagFull.replace(top,'')
        if top in tagFull:
            for excluded in list_exclude:
                if excluded not in tag:
                    noClash += 1
                if noClash == len(list_exclude):
                    if tagFull.count('.') < (top.count('.') + levels):
                        if withNames:
                            essName = getName(el)
                        if withID:
                            essID = getID(el)
                        foundMatches = True
                        list_matchedNodes.append([midBranch + tagFull,dropNewLines(el['description']), essName, essID])

    list_output = list()
    for el in list_matchedNodes:
        if withNames:
            essName = " [" + el[2] + "]"
        else:
            essName = ""
        if withID:
            essID = " {" + el[3] + "}"
        else:
            essID = ""
        if midBranch in el[0]:
            list_output.append(el[0] +  " ( " + el[1] + " )" + essName + essID)
        else:
            list_output.append(el[0] +  " - " + el[1])
    # Only matched nodes are interesting here.
    if len(list_output) > 0:
        list_output.sort()
        list_output[-1]=list_output[-1].replace(midBranch,endBranch)

    # Default to ESS as root description. 
    rootDescription = "ESS"
    for el in listBreakdown:
        if el['tag'] == top[:-1]:
            rootDescription = el['description']

    for el in list_output:
        if midBranch in el or endBranch in el:
            foundMatches = True
            print(el.replace(top,""))
        else:
            print(el.replace("[No essName defined.]",""))
    if not foundMatches: 
        print(endBranch + "No matched nodes.")
        
        
    # lists are refreshed per "top" loop.
    list_output.clear()
    list_matchedNodes.clear()
