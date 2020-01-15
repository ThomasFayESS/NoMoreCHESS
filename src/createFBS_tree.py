#!/usr/bin/python3
import json
import sys
import time

"""
Write a formatted tree of FBS for Control Systems contained with a particular FBS branch.
E.g. show the control system tree for an accelerator machine section
"""

def usage():
    print("usage: " + sys.argv[0] + " inName outName")
    print("-inName: JSON file containing the pre-filtered FBS nodes relevant to this FBS branch.")
    print("-outName: filename to write formatted FBS control system tree into.")
    print(".")
    print("e.g. " + sys.argv[0] + " rfq.json rfq.conf =ESS.ACC.A01")
    sys.exit(1)

if len(sys.argv) < 4:
    usage()


fbsInput=str(sys.argv[1])
fbsTree=str(sys.argv[2])
fbsPrefix=str(sys.argv[3])

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

with open("/home/iocuser/src/python/NoMoreCHESS/json/" + fbsInput) as inFile:
    list_FBS=json.load(inFile)

list_ControlSystems = list()
for node in list_FBS:
    if node['tag'] == fbsPrefix[:-1]:
        print(node['tag'] + " ( " + node['description'] + " )")
    if node['tag'].endswith(".K01"):
        indentLevel = node['level'] - nLevels 
        list_ControlSystems.append([node['tag'],indentLevel,node['description']])

list_output = list()
for sys in list_ControlSystems:
    recurse = int(sys[1])
    match = str(sys[0])
    while recurse > 1:
        # Throw away last delimited string
        iDelimiter = match.rfind('.')
        match = match[:iDelimiter]
        recurse-=1

        for node in list_FBS:
            if match == node['tag']:
                if [node['tag'], recurse,node['description']] not in list_ControlSystems: 
                    list_ControlSystems.append([node['tag'], recurse,node['description']]) 

for el in list_ControlSystems:
    el[0]=el[0].replace(fbsPrefix,"")

list_ControlSystems.sort()

list_output = list()
for el in list_ControlSystems:
    if el[1] > 1:
        list_output.append([downConnect * (el[1] - 1) + midBranch + el[0] + " ( " + el[2] + " )",el[1]])
    else:
        list_output.append([midBranch + el[0] + " ( " + el[2] + " )",el[1]])

leafNode=1
for el in reversed(list_output):
    if leafNode:
        el[0] = el[0].replace(midBranch,endBranch)
    leafNode = el[1] == 1

for el in list_output:
    print(el[0])
