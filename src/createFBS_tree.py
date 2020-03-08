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


"""
Format code
"""
def getTreeFormatting(level, formatCode, hasSibling):
  i=1
  strTreeFormat=""
  while i < level:
    if (2**i & formatCode) == (2**i):
      strTreeFormat+=downConnect
    else:
      strTreeFormat+="    "
      i+=1
    if hasSibling == "hasSibling":
      strTreeFormat += midBranch
    else:
      strTreeFormat += endBranch
    return strTreeFormat


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

# Define a "zero-base" root level for the tree structure.
rootLevel = fbsPrefix.count('.')
if rootLevel < 1:
  print("fbsPrefix invalid, exiting")
  exit(2)

downConnect = "│   "
midBranch = "├── "
endBranch = "└── "

with open(fPath + "/../json/" + inFile) as inputFile:
  list_FBS=json.load(inputFile)

#list_matchedNodes(Tag, Identation Level, Description, hasUncle, hasSibling)
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
        level = el['level'] - rootLevel
        list_matchedNodes.append([el['tag'],level,el['description'],0,0])
    else:
      print("skipping (invalid) node...")
      print(tag) 

# Recurse the FBS for ancestor nodes of each matched leaf node.
list_output = list()

for leaf in list_matchedNodes:
  level = int(leaf[1])
  leafTag = str(leaf[0])
  # Find ancestor information (tag + description)
  # Interested in parent relationships only here.

  while level > 1:
    foundParent = False
    iDelimiter = leafTag.rfind('.')
    parentTag = leafTag[:iDelimiter]
    for node in list_FBS:
      tag = node['tag']
      if parentTag == tag:
        leafTag = parentTag
        level-=1
        foundParent = True
        if [tag, level, node['description'],0,0] not in list_matchedNodes: 
          list_matchedNodes.append([tag, level, node['description'],0,0]) 
        break
    if not foundParent:
      print("Can't find parent node for tag: " + leafTag)

  
# Get sibling/uncle relationships for each node
copy_list_matchedNodes = list_matchedNodes
#foundUncle

for el in list_matchedNodes:
  leafTag = str(el[0])
  matchParent = leafTag[:leafTag.rfind('.')]
  matchGrandpa = matchParent[:matchParent[:-1].rfind('.')]
  el[4]="onlyChild"
  for check in copy_list_matchedNodes:
    if matchParent in check[0] and leafTag not in check[0]:
      # hasSibling is True
      el[4]="hasSibling"
      break

  """
  For each indentation level, check if uncle exists
  If true, then stuff bit-n true, where n = indentation level
  """
  for check in copy_list_matchedNodes:
    level = int(el[1])
    foundUncle = False
    while level > 1: 
      print("leafTag: " + leafTag)
      print("matchGrandpa: " + matchGrandpa)
      for check in copy_list_matchedNodes:
        if matchGrandpa in check[0] and matchParent not in check[0]:
          print("matchedUncle: " + check[0] + " to parent: " + matchParent + "; level = " + str(level))
          level -= 1
          matchParent = matchGrandpa
          matchGrandpa = matchGrandpa[:matchGrandpa[:-1].rfind('.')]
          leafTag = leafTag[:leafTag[:-1].rfind('.') + 1]
          foundUncle = True
          el[3] += 2**(level)
          print("level: " + str(level) + "; el[3] = " + str(el[3]))
          break
      if not foundUncle:
        print("No uncle found, level: " + str(level))
        level -= 1
        matchParent = matchGrandpa
        matchGrandpa = matchGrandpa[:matchGrandpa[:-1].rfind('.')]
   

    
list_matchedNodes.sort()

list_output = list()

for el in list_matchedNodes:
  format = getTreeFormatting(el[1],el[3],el[4])
  if format is not None:
    list_output.append(getTreeFormatting(el[1],el[3],el[4]) +  el[0] +  " ( " + el[2] + " )")

list_output[-1]=list_output[-1].replace(midBranch,endBranch)
print(fbsPrefix[:-1])
for el in list_output:
  print(el.replace(fbsPrefix,""))
