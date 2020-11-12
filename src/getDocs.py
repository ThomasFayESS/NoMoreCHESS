import xml.etree.ElementTree as ET
import argparse
import subprocess
import shlex
# Collection of local helper functions
import helpers

parser = argparse.ArgumentParser()
parser.add_argument('inFile', help ='Input file in XML format.')
parser.add_argument('tag', help = 'FBS tag to get document listing for.')
parser.add_argument('--download', nargs='?', const = True, default = None, help = 'Download all the documents found for this node.')
parser.add_argument('--docTag', help = 'Match only this document tag.')

args = parser.parse_args()
inFile = args.inFile
findTag = args.tag
download = args.download
docTag = args.docTag

fpath='../xml/'
inFile = 'fbs'
tree = ET.parse(inFile)

root = tree.getroot()

allDocTags=["chess_number", "doc_filename", "doc_link" ,"doc_title", "link_id"]

if docTag is None:
    # We will use CHESS number as a title grouping for document tag values
    displayDocTags=allDocTags[1:]
else:
    if docTag in allDocTags:
        displayDocTags = docTag
    else:
        displayDocTags = allDocTags[1:]

for childRoot in root:
    if childRoot.attrib['tag'] == findTag:
        print("%s ( %s )" % (childRoot.attrib['tag'],childRoot.attrib['description']))
        Documents = childRoot[-1]
        if Documents.tag == "documents":
            if len(Documents) == 0:
                print("No documents attached to this node.")
            for doc in Documents:
                # Found a document is attached to this node
                if doc.tag == 'document':
                    link_id =''
                    doc_filename = ''
                    chess_number = ''
                    for DocField in doc:
                        if DocField.tag == 'chess_number':
                            chess_number = DocField.text
                            if download is None:
                                print(chess_number)
                        if DocField.tag == 'link_id':
                            link_id = DocField.text
                        if DocField.tag == 'doc_filename':
                            doc_filename = DocField.text
                    if download is None:
                        for DocField in doc:
                            if DocField.tag in displayDocTags:
                                print("-> %s: %s" % (DocField.tag,DocField.text))
                    elif download:
                        if link_id is not None and doc_filename is not None:
                            wgetArgs = helpers.wgetArgs
                            wgetArgs[-3] = wgetArgs[-3].replace("{{ LINK_ID }}", '21308.51166.14592.56101')
                            wgetArgs[-1] = wgetArgs[-1].replace("{{ FILENAME }}", doc_filename) 
                            print("Downloading %s " % doc_filename)
                            subprocess.run(wgetArgs, capture_output=True)
                        else:
                            print("No meta-data for %s. Cannot download." % chess_number) 
