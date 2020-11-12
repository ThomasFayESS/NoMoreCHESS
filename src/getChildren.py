#!/usr/bin/env python3
import json
import sys
import os
import argparse
# Local collection of helper utility functions.
import helpers

def getDesc(node):
    desc = node['description'].replace('\n','')
    return " ( " + desc + " )"

def getName(node):
    if node['essName'] is None:
        return " [No essName defined.]"
    else:
        return " [" + node['essName']  + "]"

def getID(node):
    if node['id'] is not None:
        return ' {' + node['id'] + ' }'
    else:
        return "Error retrieving ID."

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('node', help = "'Root' node for listing children.")
parser.add_argument('--withNames', nargs = '?', const = True, default = None, help='Include ESS name in the output.')
parser.add_argument('--id', nargs = '?', const = True, default = None, help='Include ESS ID (ESS-#######) in the output.')
parser.add_argument('--levels', type=int, help='Number of levels underneath the root node to return.')


def dropNewLines(str):
    return str.replace('\n', ' ')

args = parser.parse_args()
inFile = args.inFile
nodeFind = args.node
nodeFind = nodeFind.upper()
withNames = args.withNames
withID = args.id
nLevels = args.levels

if nLevels is None or nLevels < 0:
    nLevels = 50

if nodeFind[-1] == '?':
    nodeFind = nodeFind[:-1]
    nLevels = 1
elif nodeFind[-1] == '$':
    nodeFind = nodeFind[:-1]
    nLevels = 0

# For formatting the matched nodes
# Use '~' to order after '=' and '+' chars in sorting
matchPrefix = "~> "

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)

rootNode = listBreakdown[0]['tag']
if rootNode not in nodeFind:
    nodeFind = rootNode + ".*"

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


#list_matchedNodes = [tag, description, essName, essID]
list_matchedNodes = list()

nodeCount_find = nodeFind.count('.')
for node in listBreakdown:
    noClash = 0
    tagFull = node['tag']
    essName=''
    essID=''
    if nodeFind in tagFull:
        if tagFull == nodeFind:
            list_matchedNodes.append(tagFull + getDesc(node))
        else:
            if withNames:
                essName = getName(node)
            else:
                essName = ''
            if withID:
                essID = getID(node)
            else:
                essID = ''
            nodeCount_tag = tagFull.count('.')
            if nodeCount_tag <= nodeCount_find + nLevels:
                list_matchedNodes.append(matchPrefix + tagFull.replace(nodeFind + '.',"") + getDesc(node) + essName + essID)
        
for node in list_matchedNodes:
    print(node)
