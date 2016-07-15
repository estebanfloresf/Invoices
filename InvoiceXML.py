import json
import uuid

from lxml import objectify
from django.utils.encoding import smart_str
import lxml
import xml.etree.ElementTree as ET
import re
import  os
import couchdb


class Invoice:

    def __init__(self):
        self.tagname = []
        self.tagcontent = []
        self.finaldict = {}
        self.bandera = 0

    #
    # Reads the XML and returns a list key | value e.g.: Tag -> Content
    #
    def ReadXml(self,root):

        for item in root.iter():
            tag = item.tag
            self.tagname.append(item.tag)
            self.tagcontent.append(item.text)

        newDict = dict(zip(self.tagname,self.tagcontent))

        return newDict

    #
    # Cleans the XML of any white space, special characters, or none values
    #
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
        self.listFiles = {}
        global path, parser, invoice, db
        path = "C:\\Users\\Esteban.Flores\\Documents\\GitHub\\Invoices\\facturas"
        parser = lxml.etree.XMLParser(encoding='utf-8', recover=True)
        db = self.DBconnect()

        invoice = Invoice()

        self.ReadXmlFiles()

    #
    # DB connection
    #
    def DBconnect(self):
        '''=========CouchDB'=========='''
        server = couchdb.Server('http://localhost:5984/')  # ('http://115.146.93.184:5984/')
        try:
            db = server.create('invoices')

        except:
            db = server['invoices']
        return db
    #
    # Read all the files in the specified folder
    #
    def ReadXmlFiles(self):
        # Open a file
        dirs = os.listdir(path)
        increase = 1
        #Rename the files to a conventional name
        for file in dirs:
            try:
                new_filename = "INV_" +str(uuid.uuid4())+".xml"
                os.rename(os.path.join(path, file), os.path.join(path, new_filename))
                increase += 1
            except: pass
        self.listFiles = dirs
        print(increase, " files has been read \n")

        #### For each file, the process of reading the internal XML begins HERE ####
        for newfile in dirs:
            try:
                tree = ET.parse(os.path.join(path, newfile), parser)
                root = tree.getroot()
                textoxml = smart_str(ET.tostring(root).lower())
                initial_XML = invoice.ReadXml(root)
                inner_XML = dict()

                for key,value in initial_XML.items():
                    match = re.search(r'xml+', str(value))
                    if (match):
                        try:
                                root2 = ET.fromstring(str(value))
                                inner_XML = invoice.ReadXml(root2)
                        except: pass


                # Merge the 2 merge_XML XMLs into one
                merge_XML = {**initial_XML,**inner_XML}

                final_XML = invoice.CleanXML(merge_XML)
                finalJSON = json.dumps(final_XML, ensure_ascii=False)

                if(self.on_data(finalJSON)==True):
                    print(file, "has been processed and saved\n")
                else:  print(file, "could not be saved\n")





            except Exception as e:
                print(e)
                print("There was a problem reading file: ", file)


    def on_data(self,data):
        finaldoc = json.loads(data)
        saved = None

        try:

            db.save(finaldoc)
            saved = True


        except Exception as e:
            print(e)
            saved = False

        return saved


# '''=========CouchDB'=========='''
# server = couchdb.Server('http://localhost:5984/')  # ('http://115.146.93.184:5984/')
# try:
#     db = server.create('invoices')
# except:
#     db = server['invoices']
A = Files()







