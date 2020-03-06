#!/usr/bin/python3
"""
Reduces the full ESS FBS to a region of interest.
For example, only look at nodes from one machine section.
"""
import json
import urllib.request
import time
import sys, os, getopt

def usage():
    print("usage: " + sys.argv[0] + " filterPrefix outName")
    print("-filterPrefix is the FBS prefix to filter nodes on.")
    print("-outName is the filename to write a JSON containing these filtered nodes.")
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

unixOptions=["f:o:"]
gnuOptions=["filterPrefix=", "outName="]

try:
  option_list, arguments = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
except getopt.error as err:
  usage()

filterPrefix=""
outName=""

for option, argument in option_list:
  if option in ("-f", "--filterPrefix"):
    filterPrefix = argument
  elif option in ("-o", "--outName"):
    outName = argument

if len(filterPrefix) < 1 or len(outName) < 1:
  usage()

fPath = os.path.dirname(os.path.realpath(__file__))

if filterPrefix[0] != '=':
    filterPrefix = "="+ filterPrefix
listReduced = list()

i=0

with open(fPath + "/../json/fbs.json") as fbsNodes:
    listFBS = json.load(fbsNodes)
    lenFBS=len(listFBS)
    print("filter")
    for node in listFBS:
        i=i+1
        if node['tag'].startswith(filterPrefix):
            listReduced.append(node)
        if i % 10000 == 0:
            print(str(i) + "/" + str(lenFBS))
    lenReduced=len(listReduced)
    print("Reduced FBS from " + str(lenFBS) + " to " + str(lenReduced) + " nodes.")
    with open(fPath + "/../json/" + outName,"w+") as outfile:
        json.dump(listReduced,outfile)
