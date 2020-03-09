#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
"""
Write a formatted tree of FBS for Control Systems contained with a particular FBS branch.
E.g. show the control system tree for an accelerator machine section
"""

def usage():
  print("usage: " + sys.argv[0] + " inName outName")
  print("-i --inFilse: JSON file containing the pre-filtered FBS nodes relevant to this FBS branch.")
  print("-f --fbsPrefix: FBS prefix to use as top-level node.")
  print("-e --exclude: FBS nodes to exclude from listing.")
  print("-l --levels: Number of levels to show results for.")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --fbsPrefix=ESS.ACC.A01.E01 --exclude '' --levels 1")
  print("e.g. " + sys.argv[0] + " --inFile=rfq.json --fbsPrefix=ESS.ACC.A01.E01 --exclude WG,W --levels 2")
  sys.exit(1)

unixOptions="i:f:e:l:"
gnuOptions=["inFile=", "fbsPrefix=", "exclude=", "levels="]

try:
  optionList, arguments = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
except getopt.error as err:
  usage()

inFile=""
fbsPrefix=""
exclude="ZZZZ"

for option, argument in optionList:
  if option in ("-i", "--inFile") or option[:3] == "--i":
    inFile = argument
  elif option in ("-f", "--fbsPrefix") or option[:3] == "--f":
    fbsPrefix = argument
  elif option in ("-e", "--exclude"):
    exclude = argument
  elif option in ("-l", "--levels"):
    levels = int(argument)




list_exclude = list()
temp = exclude.split(',')
if len(temp) == 1 and not temp[0].isalpha():
  list_exclude.append("ZZZZ")
elif len(temp) == 1 and temp[0].isalpha():
  list_exclude.append(temp[0])
else:
  list_exclude=list(temp)

if len(inFile) < 1 or len(fbsPrefix) < 1:
  usage()

if levels < 1:
  levels = 50

# Allow lazy prescription of fbsPrefix 
# And autofill any missing leading or trailing char.
if not fbsPrefix.endswith("."):
  fbsPrefix=fbsPrefix + "."
if not fbsPrefix.startswith("="):
  fbsPrefix="=" + fbsPrefix

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
  list_FBS=json.load(inputFile)

#list_matchedNodes(Tag, Description)
list_childNodes = list()

# Parse the FBS for matching nodes
for el in list_FBS:
  noClash = 0
  tag = el['tag']
  if fbsPrefix in tag:
    for excluded in list_exclude:
      
      if excluded not in tag:
        noClash += 1
    if noClash == len(list_exclude):
      if tag.count('.') < (fbsPrefix.count('.') + levels):
        list_childNodes.append([el['tag'],el['description']])


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
