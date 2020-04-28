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
  print("  -f --field: OPTIONAL (default to ID) Field to match. Valid options: all, id, essName, parent, level, modified, state, cableName, description")
  print("")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --fbsPrefix=ESS.ACC.A01.E01")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --fbsPrefix=ESS.ACC.A01.E01 --field id")
  sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--inFile')
parser.add_argument('--fbsPrefix')
parser.add_argument('--field')

args = parser.parse_args()
inFile = args.inFile
fbsPrefix = args.fbsPrefix
field = args.field

#Check inputs
if field is None:
  field = 'all'
if inFile is None:
  usage()

validFields = ['all', 'id', 'essName', 'modified', 'parent', 'level', 'state', 'cableName', 'description']

if field not in validFields:
  print("field is invalid")
  exit(1)

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
  list_FBS=json.load(inputFile)

if fbsPrefix is None:
  fbsPrefix=list_FBS[0][field]

# Allow lazy prescription of fbsPrefix 
# And autofill any missing leading character.
if not fbsPrefix.startswith("="):
  fbsPrefix="=" + fbsPrefix

#list_matchedNodes(Tag, Description)
list_childNodes = list()

# Parse the FBS for matching nodes
for el in list_FBS:
  noClash = 0
  tagFull = el['tag']
  tag = tagFull.replace(fbsPrefix,'')
  if fbsPrefix == tagFull:
    if field != 'all':
      print(el[field])
      exit(0)
    else:
      for iter in validFields:
        if iter != 'all':
          if el[iter] is None:
            value = 'null'
          else:
            value = str(el[iter])
          print(iter + ": " + value)
      exit(0)

print("no match found")
exit(1)
