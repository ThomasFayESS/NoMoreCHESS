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
gnuOptions = ["outFile"]

try:
  arguments, values = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
except getopt.error as err:
  usage()

outFile=values[0]
urllib.request.urlretrieve("https://itip.esss.lu.se/chess/fbs.json", outFile)
