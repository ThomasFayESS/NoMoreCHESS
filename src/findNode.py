#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse

# Local module
import helpers

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

def currentTagOnly(tag, lastTag):
    if lastTag == '':
        return tag
    else:
        return tag.replace(lastTag + '.', '')

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('--tag', type=str, help = "Match node by tag. Case insenstive so for example =ess.acc.a01 is ok.")
parser.add_argument('--cable', help = "Match node by cableName.")
parser.add_argument('--name', help = "Match node by essName. Case insensitive so for example rfq-010:rfs-dig-101 is ok.")
parser.add_argument('--withName', type=str, nargs = '?', const = True, default = None, help='Include ESS name in the output.')
parser.add_argument('--id', nargs = '?', const = True, default = None, help='Include ESS ID (ESS-#######) in the output.')
parser.add_argument('--naked', nargs = '?', const = True, default = None, help='Show only the matching breakdown structure tab.')
parser.add_argument('--group', type = int, help='Number of parents to show in a single row grouping. Default is 1.')

args = parser.parse_args()
inFile = args.inFile
matchTag = args.tag
if matchTag is not None:
    matchTag = matchTag.upper()
matchCable = args.cable
matchName = args.name
if matchName is not None:
    matchName = matchName.upper()
naked = args.naked
grouping = args.group

if grouping is None:
    grouping = 1
if grouping <= 0:
    grouping = 1
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

    list_parents = helpers.getAllParents(matchTag)
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
            matchedNode = {'tag': tagFull, 'desc': el['description']}
            break
    if matchCable is not None:
        if el['cableName'] == matchCable:
            matchedNode = {'tag': tagFull, 'desc': el['description']}
            break
    if matchTag is not None:
        if tagFull in list_parents:
            list_matchedParents.append({'tag': tagFull, 'desc': el['description']})
        if tagFull == matchTag:
            matchedNode = {'tag': tagFull, 'desc': el['description']}
            break

if len(matchedNode) > 0:
    if withName:
        matchedNode['desc'] += addName(el['essName'])
    if withID:
        matchedNode['desc'] += addID(el['id'])

if len(matchedNode) > 0 and matchTag is None:
    list_parentNodes = list()
    list_parents = helpers.getAllParents(matchedNode['tag'])
    list_matchedParents = list()
    for el in listBreakdown:
        tagFull = el['tag']
        if tagFull in list_parents:
            list_matchedParents.append({'tag' : tagFull, 'desc': el['description']})
        if len(list_matchedParents) == len(list_parents):
            break

if len(matchedNode) > 0 and len(list_matchedParents) > 0:
    strOut = ''
    if naked is None:
        print("*" * 50)
        print(matchedNode['tag'] + " ( " + matchedNode['desc'] + " ) ")
    else:
        print(matchedNode['tag'])

    if naked is None:
        print("*** Parent nodes ***")
        # Show parents in triplets for readability
        i = 1
        # Aggregate Descriptions in triplets
        aggDesc = ''
        lastTag = ''
        for parent in list_matchedParents:
            spacer = " " * (i - grouping)
            if grouping == 1:
                currentTag = currentTagOnly(parent['tag'],lastTag)
                print(" " * 2 * (i-1) + currentTag + " ( " + parent['desc'] + " )")
                lastTag = parent['tag']
            else:
                if i % grouping == 1:
                    aggDesc = parent['desc']
                else:
                    aggDesc += ' -> ' + parent['desc']
                if i % grouping == 0 or parent == list_matchedParents[-1]:
                    currentTag = currentTagOnly(parent['tag'],lastTag)
                    print(spacer + currentTag + " ( " + aggDesc + " )")
                    lastTag = parent['tag']
            i += 1
else:
    print("No matched node.")
