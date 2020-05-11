#!/usr/bin/python3
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inFile', help='Input file of FBS nodes in JSON format.')
parser.add_argument('-n', '--name', help='ESS Name to parse for matching FBS Tag. Substring matching of ESS names is supported')
parser.add_argument('-l', '--lookup', help = 'Field to lookup. Options are tag (default) and description.')

args = parser.parse_args()
inFile = args.inFile
essName = args.name
lookup = args.lookup

validLookups = ['tag', 'description']

if lookup not in validLookups:
  lookup = 'tag'

#Check inputs
if inFile is None:
  print("--inFile argument is required.")
  exit(1)
if essName is None:
  print("--name argument is required.")
  exit(1)

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
  bsFacility = json.load(inputFile)

paired_Name_Field = list()
for el in bsFacility:
  if el['essName'] != None:
    if essName in el['essName']:
      paired_Name_Field.append([el['essName'], el[lookup]])

# print output
if len(paired_Name_Field) > 1:
  for el in paired_Name_Field:
    print(str(el[0]) + " | " + str(el[1]))
else:
  print("No matching FBS node found for essName: " + essName)

