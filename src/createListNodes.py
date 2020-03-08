#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import re
"""
Write a formatted tree of FBS for Control Systems contained with a particular FBS branch.
E.g. show the control system tree for an accelerator machine section
"""

def usage():
  print("usage: " + sys.argv[0] + " inName outName")
  print("-i --inFilse: JSON file containing the pre-filtered FBS nodes relevant to this FBS branch.")
  print("-f --fbsPrefix: FBS prefix to use as top-level node.")
  print("-m --match: Match arbitrary FBS node pattern e.g. KF01")
  print("e.g. " + sys.argv[0] + " rfq.json =ESS.ACC.A01")
  sys.exit(1)


unixOptions="i:f:m:"
gnuOptions=["inFile=", "fbsPrefix=", "match="]

try:
  optionList, arguments = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
except getopt.error as err:
  print("1")
  usage()

inFile=""
fbsPrefix=""
match=""

for option, argument in optionList:
  if option in ("-i", "--inFile") or option[:3] == "--i":
    inFile = argument
  elif option in ("-f", "--fbsPrefix") or option[:3] == "--f":
    fbsPrefix = argument
  elif option in ("-m", "--match") or option[:3] == "--m":
    matchNode = argument


if len(inFile) < 1 or len(fbsPrefix) < 1 or len(matchNode) < 1:
  usage()


# match arbitary FBS nodes BUT limit substring search to four chars
if len(matchNode) > 4:
  print("FBS nodes have maximum 4 characters, exiting...")
  exit(2)

fPath = os.path.dirname(os.path.realpath(__file__))
# Allow lazy prescription of fbsPrefix 
# And autofill any missing leading or trailing char.
if not fbsPrefix.endswith("."):
  fbsPrefix=fbsPrefix + "."
if not fbsPrefix.startswith("="):
  fbsPrefix="=" + fbsPrefix

midBranch = "├── "
endBranch = "└── "

with open(fPath + "/../json/" + inFile) as inputFile:
  list_FBS=json.load(inputFile)

#list_matchedNodes(Tag, Description)
list_matchedNodes = list()

# Parse the FBS for matching nodes
for el in list_FBS:
  tag = el['tag']
  if fbsPrefix in tag:
    # Match against last branch of tree (the "leaf node").
    if '.' in tag:
      parts = tag.split('.')
      leafNode = parts[-1]
      if matchNode in leafNode:
        list_matchedNodes.append([el['tag'],el['description']])
    else:
      print("skipping (invalid) node...")
      print(tag) 

# Recurse the FBS for ancestor nodes of each matched leaf node.
list_output = list()

for leaf in list_matchedNodes:
  leafTag = str(leaf[0])
  level = leafTag.count('.') - fbsPrefix.count('.')
  # Find ancestor information (tag + description)
  # Interested in parent relationships only here.

  while level > 1:
    foundParent = False
    parentTag = leafTag[:leafTag.rfind('.')]
    for node in list_FBS:
      tag = node['tag']
      if parentTag == tag:
        leafTag = parentTag
        level-=1
        foundParent = True
        if [tag, node['description']] not in list_matchedNodes: 
          list_matchedNodes.append([tag, node['description']])
        break
    if not foundParent:
      print("Can't find parent node for tag: " + leafTag)

    
list_matchedNodes.sort()

list_output = list()

for el in list_matchedNodes:
  list_output.append(midBranch + el[0] +  " ( " + el[1] + " )")

list_output[-1]=list_output[-1].replace(midBranch,endBranch)
print(fbsPrefix[:-1])
for el in list_output:
  print(el.replace(fbsPrefix,""))
