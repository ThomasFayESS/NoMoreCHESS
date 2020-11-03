#!/usr/bin/python3
"""
Reduces the full ESS FBS to a region of interest.
For example, only look at nodes from one machine section.
"""
import json
import urllib.request
import time
import sys, os, argparse 
import fnmatch
import re
# helpers is local collection of helper functions.
from helpers import getAllParents, getRoot

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'Input JSON formatted breakdown structure to reduce based on filter specified.')
parser.add_argument('filter', help = 'prefix to filter the breakdown structure.')
parser.add_argument('outFile', help = 'Output file for the reduced breakdown structure in JSON format.')

args = parser.parse_args()

inFile = args.inFile
filter = args.filter
outFile = args.outFile

regex = fnmatch.translate(filter)
regex_compiled = re.compile(regex)


fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as fbsNodes:
  listBreakdown = json.load(fbsNodes)

lenBreakdown = len(listBreakdown)
rootNode = listBreakdown[0]['tag']
firstChar = rootNode[0]
if firstChar == '=':
    breakdown = 'fbs'
elif firstChar == '+':
    breakdown = 'lbs'
else:
    print("Breakdown structure unrecognised. Valid breakdown structures are 'fbs' and 'lbs'. Check input file is valid. Exiting...")
    exit(1)

commonRoot = getRoot(filter)
if breakdown == 'fbs':
    if commonRoot[0] != '=':
        commonRoot = '=' + commonRoot
if breakdown == 'lbs':
    if commonRoot[0] != '+':
        commonRoot = '+' + commonRoot

list_parents = getAllParents(commonRoot)

listReduced = list()
listTemp = list()

formattedTotalNodes = "{:,}".format(lenBreakdown)
print("Getting nodes under " + commonRoot)
for node in listBreakdown:
    tag = node['tag']
    if tag == commonRoot:
        listReduced.append(node)
    if tag in list_parents:
        listReduced.append(node)
    if commonRoot in tag and tag != commonRoot:
        if regex_compiled.search(tag) is not None:
            for el in listTemp:
                if el['tag'] in tag:
                    listReduced.append(el)
            listReduced.append(node)
            listTemp.clear()
        else:
            listTemp.append(node)

lenReduced=len(listReduced)
formattedReducedNodes = "{:,}".format(len(listReduced))

print("Reduced " + breakdown + " from " + formattedTotalNodes + " to " + formattedReducedNodes + " nodes.")

with open(fPath + "/../json/" + outFile,"w+") as outfile:
    json.dump(listReduced,outfile)
