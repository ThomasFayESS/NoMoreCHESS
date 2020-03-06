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
    print("-inFilse: JSON file containing the pre-filtered FBS nodes relevant to this FBS branch.")
    print("-fbsPrefix: FBS prefix to use as top-level node.")
    print("e.g. " + sys.argv[0] + " rfq.json =ESS.ACC.A01")
    sys.exit(1)



"""
Format code
"""
def getTreeFormatting(level, formatCode, hasSiblings):
    i=1
    strTreeFormat=""
    while i < level:
        if (2**i & formatCode) == (2**i):
            strTreeFormat+=downConnect
        else:
            strTreeFormat+="    "
        i+=1
    if hasSiblings:
        strTreeFormat += midBranch
    else:
        strTreeFormat += endBranch

    return strTreeFormat


unixOptions=["i:f:"]
long_options=["inFile=", "fbsPrefix="]

try:
    option_list, arguments = getopt.getopt(sys.argv[1:], unixOptions, long_options)
except getopt.error as err:
    usage()

inFile=""
fbsPrefix=""

for option, argument in option_list:
  if option in ("-i", "--inFile") or option[:3] == "--i":
    inFile = argument
  elif option in ("-f", "--fbsPrefix") or option[:3] == "--f":
    fbsPrefix = argument

if len(inFile) < 1 or len(fbsPrefix) < 1:
    usage()


fPath = os.path.dirname(os.path.realpath(__file__))
# Allow lazy prescription of fbsPrefix 
# And autofill any missing leading or trailing char.
if not fbsPrefix.endswith("."):
    fbsPrefix=fbsPrefix + "."
if not fbsPrefix.startswith("="):
    fbsPrefix="=" + fbsPrefix
nLevels=fbsPrefix.count(".")


# Formatting for pretty tree output
downConnect = "│   "
midBranch = "├── "
endBranch = "└── "

with open(fPath + "/../json/" + inFile) as inputFile:
    list_FBS=json.load(inputFile)

#list_ControlSystems(Tag, Identation Level, Description, hasUncle, hasSibling)
list_ControlSystems = list()
for node in list_FBS:
    if node['tag'] == fbsPrefix[:-1]:
        print(node['tag'] + " ( " + node['description'] + " )")
    if node['tag'][-4:-2] == ".K":
        indentLevel = node['level'] - nLevels 
        list_ControlSystems.append([node['tag'],indentLevel,node['description'],0,0])

list_output = list()
for system in list_ControlSystems:
    recurse = int(system[1])
    match = str(system[0])
    while recurse > 1:
        # Throw away trailing delimited string (leaf FBS node)
        iDelimiter = match.rfind('.')
        match = match[:iDelimiter]
        recurse-=1

        for node in list_FBS:
            if match == node['tag']:
                if [node['tag'], recurse,node['description'],0,0] not in list_ControlSystems: 
                    list_ControlSystems.append([node['tag'], recurse,node['description'],0,0]) 

# Get child/sibling relationships for each node
copy_list_ControlSystems = list_ControlSystems
time.sleep(1)
for el in list_ControlSystems:
    tag = str(el[0])
    iDelimiter = tag.rfind('.')
    matchSibling = tag[:iDelimiter +1]
    matchSiblingDelims = matchSibling.count('.')
    iDelimiter = matchSibling[:-1].rfind('.')
    matchUncle = matchSibling[:iDelimiter + 1]
    matchUncleDelims = matchUncle.count('.')
    for check in copy_list_ControlSystems:
        if matchSibling in check[0] and check[0] != tag and check[0].count('.') == matchSiblingDelims:
            el[4]=1
            break
    """
    For each indentation level, check if uncle exists
    If true, then stuff bit-n true, where n = indentation level
    """
    indentLevel = int(el[1])
    while indentLevel > 1: 
        foundUncle = 0
        for check in copy_list_ControlSystems:
            if matchUncle in check[0] and check[0].count('.') == matchUncleDelims:
                foundUncle += 1
        if foundUncle > 1:
            el[3]+=2**(indentLevel - 1)
        iDelimiter = matchUncle[:-1].rfind('.')
        matchUncle = matchUncle[:iDelimiter + 1]
        matchUncleDelims = matchUncle.count('.')

        indentLevel -= 1

list_ControlSystems.sort()

list_output = list()
for el in list_ControlSystems:
    list_output.append(getTreeFormatting(el[1],el[3],el[4]) +  el[0] +  " ( " + el[2] + " )")

list_output[-1]=list_output[-1].replace(midBranch,endBranch)
for el in list_output:
    print(el.replace(fbsPrefix,""))

