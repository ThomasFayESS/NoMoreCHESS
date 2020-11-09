import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help ='Input file in XML format.')
parser.add_argument('tag', help = 'FBS tag to get document listing for.')

args = parser.parse_args()
inFile = args.inFile
findTag = args.tag

fpath='../xml/'
inFile = 'fbs'
tree = ET.parse(inFile)

root = tree.getroot()
title,doc_id,link,filename = '','','',''

for childRoot in root:
    if childRoot.attrib['tag'] == findTag:
        print("%s ( %s )" % (childRoot.attrib['tag'],childRoot.attrib['description']))
        elDocuments = childRoot[-1]
        if elDocuments.tag == "documents":
            if len(elDocuments) == 0:
                print("No documents attached to this node.")
            for doc in elDocuments:
                if doc.tag == 'document':
                    for elDoc in doc:
                        if elDoc.tag =='chess_number':
                            if elDoc.text is not None:
                                id = elDoc.text
                            else:
                                id = 'No ID found.'
                            print(id)
                        elif elDoc.tag == 'doc_title':
                            title = elDoc.text
                            if elDoc.text is not None:
                                title = elDoc.text
                            else:
                                title = 'No title found' 
                        elif elDoc.tag == 'doc_filename':
                            if elDoc.text is not None:
                                filename = elDoc.text
                            else:
                                filename = 'No filename found'
                    print(" -> title: " + title)
                    print(" -> filename: " + filename)
            exit()
