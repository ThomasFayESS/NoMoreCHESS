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

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('pattern', nargs='?', help = "Allows specification of top node(s) by wildcard. For example '*E??.E01.K01'.")
parser.add_argument('--levels', type=int, help='Number of levels to show results for. Default is 1 level below root note.')
parser.add_argument('--withNames', nargs = '?', const = True, default = None, help='Include ESS name in the output.')
parser.add_argument('--id', nargs = '?', const = True, default = None, help='Include ESS ID (ESS-#######) in the output.')
parser.add_argument('--parents', type=int, help = 'Number of parent nodes to show for context. Default is two.')

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
levels = args.levels
withNames = args.withNames
withID = args.id
parents = args.parents

if pattern is None:
    pattern = "*"
pattern = pattern.upper()

if pattern[-1] == '$':
   levels = 0 

# For formatting the matched nodes.
# Use '~' character to preserve sorting order after '=' and '+' chars

if levels is None or levels < 0:
    levels = 50

if parents is None:
    parents = 2
if parents < 0:
    parents = 50

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)

rootNode = listBreakdown[0]['tag']

matchRoot = helpers.getRoot(pattern)
nodeCount_match = matchRoot.count('.')

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

regex = fnmatch.translate(pattern)
regex_compiled = re.compile(pattern)

#list_matchedNodes = [tag, description, essName, essID]
list_matchedNodes = list()
# Parse the breakdown structure for matching nodes
foundMatches = False
for index,node in enumerate(listBreakdown):
    noClash = 0
    tagFull = node['tag']
    essName=''
    essID=''
    # Remember to strip the trailing '.' from matchRoot
    if regex_compiled.search(tagFull):
        tag = tagFull.replace(matchRoot + '.','')
        nodeCount_tag = tagFull.count('.')

        if nodeCount_tag <= nodeCount_match + levels:
            foundMatches = True
            if withNames:
                essName = getName(node)
            if withID:
                essID = getID(node)
            list_matchedNodes.append([tag, node['description'], essName, essID])
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
    list_output.append(node[0] +  " ( " + node[1] + " )" + essName + essID)

print(matchRoot)
for node in list_output:
    foundMatches = True
    print(node)

if not foundMatches and levels != 0:
    print("No matched nodes.")
