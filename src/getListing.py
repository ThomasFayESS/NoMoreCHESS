#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse
import fnmatch
import re
# Local collection of helper utility functions.
import helpers

def checkExclusions(tag, list_exclude):
    for excludedTag in list_exclude:
        if excludedTag in tag:
            return False
    return True

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('pattern', nargs='?', help = "Allows specification of top node(s) by wildcard. For example '*E??.E01.K01'.")
parser.add_argument('--exclude', help ='Specifies the nodes to be exlucded. Can be a single node IDs or a comma seperated list. For example --exclude K for single node and --example K,KF,WG for a listing.')
parser.add_argument('--levels', type=int, help='Number of levels to show results for. Default is 1 level below root note.')
parser.add_argument('--withNames', nargs = '?', const = True, default = None, help='Include ESS name in the output.')
parser.add_argument('--id', nargs = '?', const = True, default = None, help='Include ESS ID (ESS-#######) in the output.')
parser.add_argument('--orphan', nargs ='?', const = True, default = None, help = 'Only show matches. Parent nodes added by default to give context are not shown.')

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
pattern = args.pattern
exclude = args.exclude
levels = args.levels
withNames = args.withNames
withID = args.id
orphan = args.orphan

if pattern is None:
    pattern = "*"
elif pattern[-1] == '$':
   levels = 0 

# For formatting the matched nodes
midBranch = "├── "
endBranch = "└── "


if exclude is None:
    exclude="ZZZZ"

if levels is None:
    levels = 1
elif levels < 0:
    levels = 50

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)

rootNode = listBreakdown[0]['tag']
if rootNode not in pattern:
    pattern = rootNode + ".*"

matchRoot = helpers.getRoot(pattern) + '.'

#Handle special case of '++ESS.A' in LBS
if rootNode[:2] == '++':
    rootNode = rootNode.replace('++ESS.','+ESS.')

leadingChar = listBreakdown[0]['tag'][0]

if leadingChar == '=':
    breakdown = 'fbs'
    if rootNode[0] != '=':
        rootNode = '=' + rootNode
elif leadingChar == '+':
    breakdown = 'lbs'
    if rootNode[0] != '+':
        rootNode = '+' + rootNode
else:
    print("Breakdown structure unsupported.")
    exit()



list_exclude = list()
temp = exclude.split(',')
if len(temp) == 1 and not temp[0].isalpha():
    list_exclude.append("ZZZZ")
elif len(temp) == 1 and temp[0].isalpha():
    list_exclude.append(temp[0])
else:
    list_exclude=list(temp)


# Predefine the qualifier nodes for matching from the full node tree.
list_parents = helpers.getAllParents(matchRoot)
list_parents.append(rootNode)

regex = fnmatch.translate(pattern)
regex_compiled = re.compile(pattern)

#list_matchedNodes = [tag, description, essName, essID]
list_matchedNodes = list()
# list_temp to get potential parent nodes
list_temp = list()
# Parse the breakdown structure for matching nodes
foundMatches = False
for node in listBreakdown:
    noClash = 0
    tagFull = node['tag']
    essName=''
    essID=''
    # Get parent nodes to qualify context
    if tagFull in list_parents:
        list_matchedNodes.append([node['tag'],dropNewLines(node['description']),"", ""])
    else:
        if rootNode in tagFull:
            if regex_compiled.search(tagFull):
                tag = tagFull.replace(matchRoot,'')
                if checkExclusions(list_exclude,tag):
                    if tagFull.count('.') < (matchRoot.count('.') + levels  ):
                        foundMatches = True
                        if withNames:
                            essName = getName(node)
                        if withID:
                            essID = getID(node)
                        if orphan is None:
                            for tempNode in list_temp:
                                if tempNode['tag'] in tagFull:
                                    print(tempNode['tag'])
                                    list_matchedNodes.append([tempNode['tag'],dropNewLines(tempNode['description']),"", ""])
                            list_temp.clear()
                        list_matchedNodes.append([midBranch + tag,dropNewLines(node['description']), essName, essID])
        else:
            if orphan is None:
                list_temp.append(node)
list_output = list()
for node in list_matchedNodes:
    if withNames:
        essName = " [" + node[2] + "]"
    else:
        essName = ""
    if withID:
        essID = " {" + node[3] + "}"
    else:
        essID = ""
    if midBranch in node[0]:
        list_output.append(node[0] +  " ( " + node[1] + " )" + essName + essID)
    else:
        list_output.append(node[0] +  " - " + node[1])
# Only matched nodes are interesting here.
if len(list_output) > 0:
    list_output.sort()
    list_output[-1]=list_output[-1].replace(midBranch,endBranch)

for node in list_output:
    if midBranch in node or endBranch in node:
        foundMatches = True
        print(node.replace(rootNode + '.',""))
    else:
        print(node.replace("[No essName defined.]",""))

if not foundMatches and levels != 0:
    print(endBranch + "No matched nodes.")
