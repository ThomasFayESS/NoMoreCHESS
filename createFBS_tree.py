#!/usr/bin/python3
import json
import sys

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
downConnect = "│  "
midBranch = "├── "
endBranch = "└── "


with open(fbsInput) as inFile:
    listFBS=json.load(inFile)

print(fbsPrefix[:-1])
for node in listFBS:
    if node['tag'] == fbsPrefix[:-1]:
        print(node['tag'] + " ( " + node['description'] + " )")
    if node['tag'].endswith("K01"):
        indentLevel = node['level'] - nLevels 
        if indentLevel == 1:
            print(midBranch + node['tag'].replace(fbsPrefix,"") + " (" + node['description'] + ")")

