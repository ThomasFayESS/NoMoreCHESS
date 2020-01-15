#!/usr/bin/python3
"""
Fetches ESS FBS from available JSON url
"""
import urllib.request
urllib.request.urlretrieve("https://itip.esss.lu.se/chess/fbs.json", "fbs.json")
