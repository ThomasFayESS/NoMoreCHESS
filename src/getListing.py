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
  print("Get a listing of FBS nodes contained underneath a particular FBS branch as descendant relationship.")
  print("E.g. show nodes contained within System X.")
  print("Exlusion of node patterns and specification of the number of nested levels to return are supported.")
  print("")
  print("  -i --inFile:     JSON file containing the pre-filtered FBS nodes relevant to this FBS branch.")
  print("  -f --fbsPrefix:  OPTIONAL (default to root node) FBS prefix to use as top-level node.")
  print("  -e --exclude:    OPTIONAL (default exclude none) FBS nodes to exclude from listing, empty string for no exlusions, supports list format as comma separated values.")
  print("  -l --levels:     OPTIONAL (default levels = 1) Number of levels to show results for. Integers < 1 means show all available levels.")
  print("")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --fbsPrefix=ESS.ACC.A01.E01 --exclude '' --levels 1")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --fbsPrefix=ESS.ACC.A01.E01 --exclude WG,W --levels 2")
  sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--inFile')
parser.add_argument('--fbsPrefix')
parser.add_argument('--exclude')
parser.add_argument('--levels', type=int, help='Number of levels to show results for. Default is 1')

args = parser.parse_args()
inFile = args.inFile
fbsPrefix = args.fbsPrefix
exclude = args.exclude
levels = args.levels

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
  list_FBS=json.load(inputFile)

if fbsPrefix is None:
  fbsPrefix=list_FBS[0]['tag']

# Allow lazy prescription of fbsPrefix 
# And autofill any missing leading or trailing char.
if not fbsPrefix.endswith("."):
  fbsPrefix=fbsPrefix + "."
if not fbsPrefix.startswith("="):
  fbsPrefix="=" + fbsPrefix

#list_matchedNodes(Tag, Description)
list_childNodes = list()

# Parse the FBS for matching nodes
for el in list_FBS:
  noClash = 0
  tagFull = el['tag']
  tag = tagFull.replace(fbsPrefix,'')
  if fbsPrefix in tagFull:
    for excluded in list_exclude:
      if excluded not in tag:
        noClash += 1
    if noClash == len(list_exclude):
      if tagFull.count('.') < (fbsPrefix.count('.') + levels):
        list_childNodes.append([tagFull,el['description']])

list_output = list()

midBranch = "├── "
endBranch = "└── "

for el in list_childNodes:
  list_output.append(midBranch + el[0] +  " ( " + el[1] + " )")

if len(list_output) <1:
  print("No matches found.")
  exit(0)


list_output.sort()
list_output[-1]=list_output[-1].replace(midBranch,endBranch)

for el in list_FBS:
  if el['tag'] == fbsPrefix[:-1]:
    rootDescription = el['description']

print(fbsPrefix[:-1] + " ( " + rootDescription + " ) ")
for el in list_output:
  print(el.replace(fbsPrefix,""))