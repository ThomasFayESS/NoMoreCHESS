#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import re


def usage():
  print("usage: " + sys.argv[0] + " [options] ")
  print("Get a listing of all nodes underneath a top-level node that match a node pattern")
  print("Input arguments are ALL REQUIRED. No arguments are optional")
  print("")
  print("  -i --inFilse: JSON file containing the pre-filtered FBS nodes relevant to this FBS branch.")
  print("  -f --fbsPrefix: FBS prefix to use as top-level node. Leading '=' is optional.")
  print("  -m --match: Match arbitrary FBS node pattern e.g. KF01 or KF or WG. Lists are supported as comma separated value inputs, see example below")
  print("")
  print("e.g. " + sys.argv[0] + " --inFile rfq.json --fbsPrefix ESS.ACC.A01 --match WG")
  print("e.g. " + sys.argv[0] + " --inFile rfq.json --fbsPrefix ESS.ACC.A01 --match WG,WH,WG")
  sys.exit(1)


unixOptions="i:f:m:"
gnuOptions=["inFile=", "fbsPrefix=", "match="]

try:
  optionList, arguments = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
except getopt.error as err:
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

temp=matchNode.split(',')
list_matchNodes = list()
if len(temp) == 0:
  print("Invalid match definition, exiting...")
  exit(2)
elif len(temp) == 1:
  list_matchNodes.append(matchNode)
else:
  for el in temp:
    list_matchNodes.append(el)

# match arbitary FBS nodes BUT limit substring search to four chars
for matchNode in list_matchNodes:
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
for matchNode in list_matchNodes:
  for el in list_FBS:
    tag = el['tag']
    if fbsPrefix in tag:
      # Match against last branch of tree (the "leaf node").
      leafNode = tag.split('.')[-1]
      leafNodeComponent = re.sub("[0-9]", "", leafNode)
      if matchNode == leafNodeComponent:
        list_matchedNodes.append([el['tag'],el['description']])

  # Recurse the FBS for ancestor nodes of each matched leaf node.
  list_output = list()

  for leaf in list_matchedNodes:
    leafTag = str(leaf[0])
    level = leafTag.count('.') - fbsPrefix.count('.')
    # Find ancestor information (tag + description)
    # Interested in parent relationships only here.

    while level > 0:
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

for el in list_FBS:
  if el['tag'] == fbsPrefix[:-1]:
    rootDescription = el['description']

print(fbsPrefix[:-1] + " ( " + rootDescription + " ) ")
for el in list_output:
  print(el.replace(fbsPrefix,""))
