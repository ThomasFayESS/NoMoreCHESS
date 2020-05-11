#!/usr/bin/python3
"""
Reduces the full ESS FBS to a region of interest.
For example, only look at nodes from one machine section.
"""
import json
import urllib.request
import time
import sys, os, argparse 

def usage():
  print("usage: " + sys.argv[0] + " --inFile --filterPrefix --outFile")
  print("-i --inFile: input file containing FBS in JSON format.")
  print("-f --filterPrefix: Breakdown structure prefix to filter (reduce) nodes on.")
  print("-o --outFile: output file (JSON format)")
  sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--inFile')
parser.add_argument('--filterPrefix')
parser.add_argument('--outFile')

args = parser.parse_args()

inFile = args.inFile
filterPrefix = args.filterPrefix
outFile = args.outFile

if inFile is None or filterPrefix is None or outFile is None:
  usage()

fPath = os.path.dirname(os.path.realpath(__file__))

# Allow lazy formatting of prefixes (miss leading '=' char for FBS and leading '+' char for LBS."


listReduced = list()

i=0

with open(fPath + "/../json/" + inFile) as fbsNodes:
  
  listBreakdown = json.load(fbsNodes)
  lenBreakdown = len(listBreakdown)
  leadingChar = listBreakdown[0]['tag'][0]
  if leadingChar == '=':
    breakdown = 'fbs'
    if filterPrefix[0] != '=':
      filterPrefix = "="+ filterPrefix
  elif leadingChar == '+':
    breakdown = 'lbs'
    if filterPrefix[0] != '+':
      filterPrefix = '+' + filterPrefix
  else:
    print("Breakdown structure unrecognised. Valid breakdown structures are 'fbs' and 'lbs'. Check input file is valid. Exiting...")
    exit(1)

  for node in listBreakdown:
    i=i+1
    if node['tag'].startswith(filterPrefix):
      listReduced.append(node)
    if i % 10000 == 0:
      print(str(i) + "/" + str(lenBreakdown))

lenReduced=len(listReduced)
print("Reduced " + breakdown + " from " + str(lenBreakdown) + " to " + str(lenReduced) + " nodes.")
with open(fPath + "/../json/" + outFile,"w+") as outfile:
  json.dump(listReduced,outfile)
