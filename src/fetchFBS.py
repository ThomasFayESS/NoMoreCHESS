#!/usr/bin/python3
"""
Fetches ESS FBS from available JSON url
"""
import urllib.request, sys, getopt

def usage():
  print("usage " + sys.argv[0] + "-outFile")
  print("outFile    name of file for saving of FBS JSON.")
  exit(1)

if len(sys.argv) < 2:
  usage()

unixOptions = "o"
longOptions = ["outFile="]

try:
  options, arguments = getopt.getopt(sys.argv[1:], unixOptions, longOptions)
except getopt.error as err:
  usage()

for option, argument in options:
  if option in ("-o", "--outFile"):
    outFile = argument

if len(outFile) < 1:
  usage()

urllib.request.urlretrieve("https://itip.esss.lu.se/chess/fbs.json", "../json/" + outFile)
