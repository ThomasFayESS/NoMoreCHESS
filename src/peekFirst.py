#!/usr/bin/python3
import json
import sys
import time
import os
import getopt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help = 'The input JSON formatted file containing the ESS breakdown structure to parse.')
args = parser.parse_args()
inFile = args.inFile

fPath = os.path.dirname(os.path.realpath(__file__))
with open(fPath + "/../json/" + inFile) as inputFile:
    listBreakdown=json.load(inputFile)

firstEntry = listBreakdown[0]
validKeys = firstEntry.keys()
print(firstEntry['tag'])
for key in validKeys:
    print("---" + str(key) + ": " + str(firstEntry[key]))
