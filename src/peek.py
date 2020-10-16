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
args = parser.parse_args()
inFile = args.inFile
offset = args.offset
rangeNodes = args.rangeNodes

if offset is None:
    offset = 0

n1 = None
n2 = None

if rangeNodes is not None:
    temp = rangeNodes.split(',')
    n1 = int(temp[0])
    n2 = int(temp[1])

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)
lenNodes = len(listBreakdown)
validKeys = listBreakdown[0].keys()
nNodes = "{:,}".format(lenNodes)
print(nNodes + " nodes.")
if rangeNodes is None:
    print("Node " + str(offset) + ": " + listBreakdown[offset]['tag'])

if n1 is not None and n2 is not None:
    for offsetRange in range(n1,n2):
        print("Node " + str(offsetRange) + ": " + listBreakdown[offsetRange]['tag'])

