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
parser.add_argument('--everything', nargs ='?', const = True, default = None,  help = 'Show all nodes')
parser.add_argument('--countNodes', nargs ='?', const = True, default = None, help = 'Simply return the node count and exit.')
args = parser.parse_args()
countNodes = args.countNodes
inFile = args.inFile
offset = args.offset
rangeNodes = args.rangeNodes
all = args.all
everything = args.everything

n1 = 1
n2 = 1
if offset is not None:
    n1 += offset
    n2 += offset

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)
lenNodes = len(listBreakdown)
nNodes = "{:,}".format(lenNodes) + " nodes. "

if countNodes:
    print(nNodes)
    exit()

validKeys = listBreakdown[0].keys()

if everything is None:
    print(nNodes)

if rangeNodes is not None:
    temp = rangeNodes.split(',')
    try:
        n1 = int(temp[0])
    except:
        n1 = 1
    try:
        n2 = int(temp[1])
    except:
        n2 = lenNodes

if n2 > lenNodes:
    n2 = lenNodes

if everything:
    n2 = lenNodes

# Adjust for 0-base
n1 = n1 -1
n2 = n2 -1
for offsetRange in range(n1,n2 + 1):
    if everything is not None:
        leadingText=''
    else:
        leadingText = "Node " + str(offsetRange + 1) + ": "
    print(leadingText + listBreakdown[offsetRange]['tag'] + " (" + listBreakdown[offsetRange]['description'] + ")" )
    if all:
        for el in validKeys:
            fieldVal = listBreakdown[offsetRange][el] 
            if fieldVal is not None:
                print("~> " + el + ": " + str(fieldVal))
            else:
                print("~> " + el + ": " + "None")
