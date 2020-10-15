#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('--top', help = 'Defines the top node to take listing from. Can be single string or comma delimited list of strings e.g. \'A01,A02,A03\'. Specify absolute node or relative to global root note. Leading \'=\' and \'+\' characters for the relevant breakdown structure are optional.')
parser.add_argument('--exclude', help ='Specifies the nodes to be exlucded. Can be a single node IDs or a comma seperated list. For example --exclude K for single node and --example K,KF,WG for a listing.')
parser.add_argument('--levels', type=int, help='Number of levels to show results for. Default is 1')
parser.add_argument('--withNames', nargs = '?', const = True, default = None, help='Include ESS name in the output.')
parser.add_argument('--id', nargs = '?', const = True, default = None, help='Include ESS ID (ESS-#######) in the output.')
args = parser.parse_args()
inFile = args.inFile
top = args.top
exclude = args.exclude
levels = args.levels
withNames = args.withNames
withID = args.id


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

#list_childNodoes = [tag, description, essName]
list_childNodes = list()

# Parse the breakdown structure for matching nodes
for top in list_top:
    if rootNode not in top:
        top = rootNode + '.' + top
    #Handle special case of '++ESS.A' in LBS
    if top[:2] == '++':
        top = '+ESS.'
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
        tag = tagFull.replace(top,'')
        if top in tagFull:
            for excluded in list_exclude:
                if excluded not in tag:
                    noClash += 1
                if noClash == len(list_exclude):
                    if tagFull.count('.') < (top.count('.') + levels):
                        if withNames:
                            if el['essName'] is None:
                                essName = 'no ESS Name defined'
                            else:
                                essName = el['essName']
                        else:
                            essName = ''
                        if withID:
                            if el['id'] is None:
                                essID = 'no ESS ID defined'
                            else:
                                essID = el['id']
                        else:
                            essID=''
                        list_childNodes.append([tagFull,el['description'], essName, essID])
    list_output = list()
    midBranch = "├── "
    for el in list_childNodes:
        if withNames:
            essName = " [" + el[2] + "]"
        else:
            essName = ""
        if withID:
            essID = " {" + el[3] + "}"
        else:
            essID = ""
        list_output.append(midBranch + el[0] +  " ( " + el[1] + " )" + essName + essID)
    if len(list_output) <1:
        print("*** No registered nodes for " + top[:-1] + " ***")
        exit(0)

    list_output.sort()
    endBranch = "└── "
    list_output[-1]=list_output[-1].replace(midBranch,endBranch)

    # Default to ESS as root description. 
    rootDescription = "ESS"
    for el in listBreakdown:
        if el['tag'] == top[:-1]:
            rootDescription = el['description']

    print(top[:-1] + " ( " + rootDescription + " ) ")
    for el in list_output:
        print(el.replace(top,""))
    
    # lists are refreshed per "top" loop.
    list_output.clear()
    list_childNodes.clear()
