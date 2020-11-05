#!/usr/bin/python3
import json
import argparse
import os
# Local collection of helper scripts
import helpers

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('node', help = 'Find the parent nodes to this node.')
parser.add_argument('--parents', type = int, help = 'Number of parents to show. Default is all apart from top "ESS" level. Minus number mean all available apart from last n.')

args = parser.parse_args()
inFile = args.inFile
nodeFind = args.node
nodeFind = nodeFind.upper()
nParents = args.parents

endBranch = "└── "

if nodeFind[0] != '=' and nodeFind[0] != '.':
    print("1")
    print("node invalid: " + nodeFind)

for char in nodeFind[1:]:
    if not char.isalnum() and char != '.':
        print("2")
        print("node invalid: " + nodeFind)
        exit()

if nParents is None:
    nParents = -1

list_parents= helpers.getAllParents(nodeFind)
nParentsFound = len(list_parents)

if nParents == 0:
    nParents = nParentsFound
elif nParents < 0:
    nParents += nParentsFound

if nParents != 0:
    for i in range(0,nParentsFound - nParents):
        del list_parents[0]

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)


# Store tag and description for disply
list_matchedNodes = list()
for node in listBreakdown:
    if node['tag'] in list_parents:
        list_matchedNodes.append([node['tag'], node['description']])
    if node['tag'] == nodeFind:
        list_matchedNodes.append([node['tag'], node['description']])

print("*" * 10 + "Breakdown Hierarchy" + "*" * 10)
print("")
countFirstTag = list_matchedNodes[0][0].count('.')
lastTag=''

# Aggregate two tag + description combinations for display
aggTag = ''
aggDesc = ''

isEven = len(list_matchedNodes) % 2 == 0
if isEven:
    i=1
else:
    i=0

for node in list_matchedNodes:
    tag = node[0]
    description = node[1]

    countTag = tag.count('.')
    spacer = (countTag - countFirstTag - 1) * 2
    spacer = " " * spacer
    if node == list_matchedNodes[-1]:
        print("  " + spacer + endBranch + tag.replace(lastTag,'') + " ( " + description + " ) ")

    elif i % 2 == 1:

        if i == 1:
            prefix = ''
        else:
            prefix = spacer + endBranch

        if aggTag == '':
            if lastTag == '':
                aggTag = prefix + tag
                aggDesc = " ( " + description + " ) "
            else:
                aggTag = " " * 3 + prefix + tag.replace(lastTag,'')
        else:
            aggTag = prefix + aggTag + '.' + tag.replace(lastTag,'')
            aggDesc = " ( " + aggDesc + " ; " + description + " ) "

        if node == list_matchedNodes[-1]:
            aggTag = aggTag[1:]

        print(aggTag + aggDesc)
    
        last_aggTag = aggTag
        aggTag = ''
        aggDesc = ''
            
    else:
        aggTag = tag.replace(lastTag,'')
        aggDesc = description 
    lastTag = tag + '.'
    i += 1
