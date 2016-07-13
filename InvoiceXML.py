from lxml import objectify
from xml.sax.saxutils import escape, unescape
from django.utils.encoding import smart_str
import lxml
import xml.etree.ElementTree as ET
import re
import  os, sys


class Invoice:

    def __init__(self):
        self.tagname = []
        self.tagcontent = []
        self.finaldict = {}
        self.bandera = 0



    def ReadXml(self,root):

        for item in root.iter():
            tag = item.tag
            self.tagname.append(item.tag)
            self.tagcontent.append(item.text)

        newDict = dict(zip(self.tagname,self.tagcontent))

        return newDict


    def CleanXML(self,tobecleaned):
     cleanedone = dict(tobecleaned)
     for key,value in tobecleaned.items():

         # Clean out xml elements
         match = re.search(r'xml+', str(value))
         if (match):
             try:
                del cleanedone[key]
             except Exception as e: pass

         # Clean out http elements of the key
         match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(key))
         if (match):
             try:
                 del cleanedone[key]
             except Exception as e:  pass

         # Clean out http elements of the values
         match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(value))
         if (match):
             try:
                 del cleanedone[key]
             except Exception as e: pass

         # Clean out white spaces
         match = re.match(r'\s+', str(value))
         if (match):
             try:
                 del cleanedone[key]
             except Exception as e: pass

         # Clean out none values
         match = re.match(r'None+', str(value))
         if (match):
             try:
                 del cleanedone[key]
             except Exception as e:           pass

     return cleanedone

class Files:

    def __init__(self):
        self.ReadXmlFiles()
        A = Invoice()



    def ReadXmlFiles(self):
        # Open a file
        path = "C:\\Users\\Esteban.Flores\\Documents\\GitHub\\UsefulTools\\facturas"
        dirs = os.listdir(path)

        sizeFolder = len(dirs)
        for file in dirs:
            print(file)


parser = lxml.etree.XMLParser(encoding='utf-8',recover=True)
tree = ET.parse("facturas/foo.xml",parser)
root = tree.getroot()
textoxml = smart_str(ET.tostring(root).lower())
Invoice = Invoice()

initial_XML = Invoice.ReadXml(root)
inner_XML = dict()

#Search inside of the current XML in case there is more xml tags information
for key,value in initial_XML.items():
    if ("xml version" in str(value)):
        try:
            root2 = ET.fromstring(str(value))
            inner_XML = Invoice.ReadXml(root2)
        except Exception as e:  print(e)




# Merge the 2 merge_XML XMLs into one
merge_XML = {**initial_XML,**inner_XML}


new = Invoice.CleanXML(merge_XML)

for i,j in new.items():
    print(i,"---",str(j).strip())



