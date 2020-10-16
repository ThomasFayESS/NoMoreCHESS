#!/usr/bin/python3
"""
Reduces the full ESS FBS to a region of interest.
For example, only look at nodes from one machine section.
"""
import json
import urllib.request
import time
import sys, os, argparse 

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'Input JSON formatted breakdown structure to reduce based on filter specified.')
parser.add_argument('filter', help = 'prefix to filter the breakdown structure.')
parser.add_argument('outFile', help = 'Output file for the reduced breakdown structure in JSON format.')

args = parser.parse_args()

inFile = args.inFile
filter = args.filter
outFile = args.outFile

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


list_filter = list()
temp = filter.split(',')
if len(temp) == 1:
    list_filter.append(temp[0])
else:
    list_filter = list(temp)


nFilters = len(list_filter)
for i in range(0,nFilters):
    if not list_filter[i].startswith(rootNode):
        list_filter[i] = rootNode + '.' + list_filter[i]
    
#Get the common root node of the filter patterns
minLength=99999
shortestFilter=""
for el in list_filter:
    if len(el) < minLength:
        minLength = len(el)
        shortestFilter = el

if len(list_filter) > 1:
    commonRoot = False
    while not commonRoot:
        commonRoot = True
        for el in list_filter:
            if shortestFilter not in el:
                commonRoot = True
        temp = shortestFilter.split('.')
        for i in range(0, len(temp) -1 ):
            if i == 0:
                shortestFilter = temp[i]
            else:
                shortestFilter += "." + temp[i]
else:
    shortestFilter='ZzZzZ'


listReduced = list()

formattedTotalNodes = "{:,}".format(lenBreakdown)
for elFilter in list_filter:
    i = 0
    print("Getting nodes under " + elFilter)
    for node in listBreakdown:
        i=i+1
        if node['tag'] == shortestFilter:
            listReduced.append(node)
        if node['tag'].startswith(elFilter):
            listReduced.append(node)
        if i % 10000 == 0:
            print("{:,}".format(i) + "/" + formattedTotalNodes)

lenReduced=len(listReduced)
formattedReducedNodes = "{:,}".format(len(listReduced))

print("Reduced " + breakdown + " from " + formattedTotalNodes + " to " + formattedReducedNodes + " nodes.")

with open(fPath + "/../json/" + outFile,"w+") as outfile:
    json.dump(listReduced,outfile)
