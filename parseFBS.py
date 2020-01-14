#!/usr/bin/python3
import json
import urllib.request
import time
with open("./fbs.json") as fbsNodes:
    print(type(fbsNodes))
    print(fbsNodes)
    listFBS = json.load(fbsNodes)
    with open("fbsNodes.conf","w+") as outfile:
        for node in listFBS:
            outfile.write(node['tag'] + " " + node['description'] + "\n")

"""
with urllib.request.urlopen("https://itip.esss.lu.se/chess/fbs.json") as url:
    nodesFBS_JSON = json.loads(url.read().decode())
    with open("./fbs_decode.json", "w+") as outfile:
        outfile.write(str(nodesFBS_JSON))
"""
