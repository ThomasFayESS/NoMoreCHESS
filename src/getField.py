#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inFile', help='Input file of FBS nodes in JSON format.')
parser.add_argument('-n', '--node', help='Breakdown structure node to match. This is exact match only, however the leading \'=\' character does not need to be specified.')
parser.add_argument('-f', '--field', help='Type of FBS field to match (default is all), supported FBS fields are id, essName, parent, modified, state, cableName, description, level, all. Support LBS fields are description, id, level, modified, parent, state tag, type, all.')
parser.add_argument('-r', '--parent', action='store_const', const=True, help='Parent flag, include this flag to look to the specified node\'s parent.')

args = parser.parse_args()
inFile = args.inFile
node = args.node
field = args.field
parent = args.parent


#Check inputs
if field is None:
  field = 'all'
if parent is None:
  parent = False
if inFile is None:
  print("--inFile argument is required.")
  exit(1)

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
  listBreakdown=json.load(inputFile)

leadingChar = listBreakdown[0]['tag'][0]
if leadingChar == '=':
  breakdown = 'fbs'
elif leadingChar == '+':
  breakdown = 'lbs'


validFieldsFBS = ['all', 'id', 'essName', 'modified', 'parent', 'level', 'state', 'cableName', 'description']
validFieldsLBS = ['all', 'description', 'id', 'level', 'modified', 'parent', 'state', 'tag', 'type']

if breakdown == 'fbs':
  validFields = validFieldsFBS
elif breakdown == 'lbs':
  validFields = validFieldsLBS

if field not in validFields:
  print("field is invalid")
  exit(1)

if node is None:
  node=listBreakdown[0]['tag']

if parent:
  if node.count('.') > 0:
    node=node[:node.rfind('.')]
  else:
    print("node invalid")
    exit(1)
     

# Allow lazy prescription of node 
# And autofill any missing leading character.
if not node.startswith('=') and not node.startswith('+') :
  if breakdown == 'fbs': 
    node = '=' + node
  if breakdown == 'lbs':
    node = '+' + node


#list_matchedNodes(Tag, Description)
list_childNodes = list()

# Parse the FBS for matching nodes
for el in listBreakdown:
  noClash = 0
  tagFull = el['tag']
  tag = tagFull.replace(node,'')
  if node == tagFull:
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
