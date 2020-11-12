#!/usr/bin/python3
"""
Fetches ESS FBS from available JSON url
Unix style and GNU style options are valid.
"""
import urllib.request, sys, argparse

def usage():
  print("usage " + sys.argv[0] + "-outFile")
  print("-o --outFile    name of file for saving of resultant FBS JSON.")
  exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('outFile', help ='Output file for the resultant breakdown listing in JSON format.')
parser.add_argument('--breakdown',help="breakdown: valid options are 'fbs' or 'lbs'.")
parser.add_argument('--source',help="Data source, either json (default) or XML endpoint available.")

args = parser.parse_args()
outFile = args.outFile
breakdown = args.breakdown
source = args.source

if breakdown is None:
  if 'fbs' in outFile:
    breakdown = 'fbs' 
  if 'lbs' in outFile:
    breakdown = 'lbs'

if source is None:
    source='json'

validSources=["json", "xml"]
validBreakdowns=["fbs", "lbs"]

if breakdown not in validBreakdowns:
  print("Only 'fbs' and 'lbs' are valid breakdown structures for fetching.")
  exit(1)

if source not in validSources:
    print("Only JSON and XML sources are available.")
    exit(1)

urllib.request.urlretrieve("https://itip.esss.lu.se/chess/" + breakdown  + "." + source, "../" + source + "/" + outFile)
