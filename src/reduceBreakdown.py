#!/usr/bin/python3
"""
Reduces the full ESS FBS to a region of interest.
For example, only look at nodes from one machine section.
"""
import json
import urllib.request
import time
import sys, os, argparse 

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'Input JSON formatted breakdown structure to reduce based on filterPrefix specified.')
parser.add_argument('filterPrefix', help = 'prefix to filter the breakdown structure.')
parser.add_argument('outFile', help = 'Output file for the reduced breakdown structure in JSON format.')

args = parser.parse_args()

inFile = args.inFile
filterPrefix = args.filterPrefix
outFile = args.outFile

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
