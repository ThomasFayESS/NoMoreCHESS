#!/usr/bin/python3
"""
Reduces the full ESS FBS to a region of interest.
For example, only look at nodes from one machine section.
"""
import json
import urllib.request
import time
import sys, os, getopt
import fnmatch

def usage():
  print("usage: " + sys.argv[0] + " --inFile --filterPrefix --outFile")
  print("-i --inFile: input file containing FBS in JSON format.")
  print("-f --filterPrefix: FBS prefix to filter (reduce) nodes on.")
  print("-o --outFile: output file (JSON format)")
  sys.exit(1)

if len(sys.argv) < 3:
  usage()

unixOptions=["i:f:o:"]
gnuOptions=["inFile=", "filterPrefix=", "outFile="]

try:
  option_list, arguments = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
except getopt.error as err:
  usage()

inFile=""
filterPrefix=""
outFile=""

for option, argument in option_list:
  if option in ("-i", "--inFile"):
    inFile = argument
  elif option in ("-f", "--filterPrefix"):
    filterPrefix = argument
  elif option in ("-o", "--outFile"):
    outFile = argument

if len(inFile) < 1 or len(filterPrefix) < 1 or len(outFile) < 1:
  usage()

fPath = os.path.dirname(os.path.realpath(__file__))

if filterPrefix[0] != '=':
  filterPrefix = "="+ filterPrefix
listReduced = list()

i=0

with open(fPath + "/../json/" + inFile) as fbsNodes:
  listFBS = json.load(fbsNodes)
  lenFBS=len(listFBS)
  for node in listFBS:
    i=i+1
    if node['tag'].startswith(filterPrefix):
      listReduced.append(node)
    if i % 10000 == 0:
      print(str(i) + "/" + str(lenFBS))

lenReduced=len(listReduced)
print("Reduced FBS from " + str(lenFBS) + " to " + str(lenReduced) + " nodes.")
with open(fPath + "/../json/" + outFile,"w+") as outfile:
  json.dump(listReduced,outfile)
