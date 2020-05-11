#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse
"""
"""

def usage():
  print("usage: " + sys.argv[0] + " [options]")
  print("Get a listing of breakdown structure nodes contained underneath a particular breakdown structure branch as descendant relationship.")
  print("E.g. show nodes contained within System X.")
  print("Exlusion of node patterns and specification of the number of nested levels to return are supported.")
  print("")
  print("  -i --inFile:     JSON file containing the pre-filtered breakdown structure (using reduceBreakdown.py) nodes relevant to this branch.")
  print("  -f --filterPrefix:  OPTIONAL (default to root node) Breakdown structure prefix to use as top-level node.")
  print("  -e --exclude:    OPTIONAL (default exclude none) Breakdown structure nodes to exclude from listing, empty string for no exlusions, supports list format as comma separated values.")
  print("  -l --levels:     OPTIONAL (default levels = 1) Number of levels to show results for. Integers < 1 means show all available levels.")
  print("  -r --relative:   OPTIONAL define filter prefix relative to root node of input JSON.")
  print("")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --filterPrefix=ESS.ACC.A01.E01 --exclude '' --levels 1")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --filterPrefix=ESS.ACC.A01.E01 --exclude WG,W --levels 2")
  sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--inFile')
parser.add_argument('--filterPrefix')
parser.add_argument('--exclude')
parser.add_argument('--levels', type=int, help='Number of levels to show results for. Default is 1')
parser.add_argument('--relative')

args = parser.parse_args()
inFile = args.inFile
filterPrefix = args.filterPrefix
exclude = args.exclude
levels = args.levels
relative = args.relative

if exclude is None:
  exclude="ZZZZ"

if levels is None:
  levels = 1
elif levels < 1:
  levels = 50

list_exclude = list()
temp = exclude.split(',')
if len(temp) == 1 and not temp[0].isalpha():
  list_exclude.append("ZZZZ")
elif len(temp) == 1 and temp[0].isalpha():
  list_exclude.append(temp[0])
else:
  list_exclude=list(temp)

if inFile is None:
  usage()

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
  listBreakdown=json.load(inputFile)

leadingChar = listBreakdown[0]['tag'][0]

if filterPrefix is None:
  filterPrefix=listBreakdown[0]['tag']
if relative is not None:
  filterPrefix = listBreakdown[0]['tag'] + '.' + relative

#Handle special case of '++ESS.A' in LBS
if filterPrefix[:2] == '++':
  filterPrefix = '+ESS.'

# Allow lazy prescription of filterPrefix 
# And autofill any missing leading or trailing char.
if not filterPrefix.endswith("."):
  filterPrefix=filterPrefix + "."
if leadingChar == '=':
  if filterPrefix[0] != '=':
    breakdown = 'lbs'
    filterPrefix = "=" + filterPrefix
elif leadingChar == '+':
  if filterPrefix[0] != '+':
    filterPrefix = '+' + filterPrefix
    breakdown = 'fbs'
else:
  print("Input file is unsupported. Must be 'lbs' or 'fbs' breakdown structure.")
  exit(1) 

#list_childNodoes = [tag, description]
list_childNodes = list()

# Parse the breakdown structure for matching nodes
for el in listBreakdown:
  noClash = 0
  tagFull = el['tag']
  tag = tagFull.replace(filterPrefix,'')
  if filterPrefix in tagFull:
    for excluded in list_exclude:
      if excluded not in tag:
        noClash += 1
    if noClash == len(list_exclude):
      if tagFull.count('.') < (filterPrefix.count('.') + levels):
        list_childNodes.append([tagFull,el['description']])

list_output = list()

midBranch = "├── "

for el in list_childNodes:
  list_output.append(midBranch + el[0] +  " ( " + el[1] + " )")

if len(list_output) <1:
  print("No matches found.")
  exit(0)

list_output.sort()
endBranch = "└── "
list_output[-1]=list_output[-1].replace(midBranch,endBranch)

# Default to ESS as root description. 
rootDescription = "ESS"
for el in listBreakdown:
  if el['tag'] == filterPrefix[:-1]:
    rootDescription = el['description']

print(filterPrefix[:-1] + " ( " + rootDescription + " ) ")
for el in list_output:
  print(el.replace(filterPrefix,""))
