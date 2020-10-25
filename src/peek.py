#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
parser.add_argument('--offset', type=int, help = 'Peek into file with offset n from first node.')
parser.add_argument('--rangeNodes', help ='Peek into file with offset n1 to n2. e.g. \'0,5\'')
parser.add_argument('--all', nargs ='?', const = True, default = None,  help = 'Show all fields')
args = parser.parse_args()
inFile = args.inFile
offset = args.offset
rangeNodes = args.rangeNodes
all = args.all

if offset is None:
    offset = 0

n1 = offset
n2 = offset + 1

if rangeNodes is not None:
    temp = rangeNodes.split(',')
    n1 = int(temp[0])
    n2 = int(temp[1]) + 1


fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)
lenNodes = len(listBreakdown)
validKeys = listBreakdown[0].keys()
nNodes = "{:,}".format(lenNodes)
print(nNodes + " nodes.")

for offsetRange in range(n1,n2):
    print("Node " + str(offsetRange) + ": " + listBreakdown[offsetRange]['tag'] + " (" + listBreakdown[offsetRange]['description'] + ")" )
    if all:
        for el in validKeys:
            fieldVal = listBreakdown[offsetRange][el] 
            if fieldVal is not None:
                print("-> " + el + ": " + str(fieldVal))
            else:
                print("-> " + el + ": " + "None")
