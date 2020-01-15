#!/usr/bin/python3
"""
Reduces the full ESS FBS to a region of interest.
For example, only look at nodes from one machine section.
"""
import json
import urllib.request
import time
import sys

def usage():
    print("usage: " + sys.argv[0] + " filterPrefix outName")
    print("-filterPrefix is the FBS prefix to filter nodes on.")
    print("-outName is the filename to write these filtered nodes to.")
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

filterPrefix=str(sys.argv[1])
outName=str(sys.argv[2])

listReduced = list()

i=0
with open("./fbs.json") as fbsNodes:
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
    with open(outName,"w+") as outfile:
        json.dump(listReduced,outfile)
