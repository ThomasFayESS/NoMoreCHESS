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
parser.add_argument('--outFile')
parser.add_argument('--breakdown',help="breakdown: valid options are 'fbs' or 'lbs'.")

args = parser.parse_args()
outFile = args.outFile
breakdown = args.breakdown

validBreakdowns=["fbs", "lbs"]
if breakdown not in validBreakdowns:
  print("Only 'fbs' and 'lbs' are valid breakdown structures for fetching.")
  exit(1)

if outFile is None:
  print("--outFile is not optional.")
  exit(1)
urllib.request.urlretrieve("https://itip.esss.lu.se/chess/" + breakdown  + ".json", "../json/" + outFile)
