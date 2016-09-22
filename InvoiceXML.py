import json
import uuid
from pymongo import MongoClient

import xmltodict as xmltodict
from django.utils.encoding import smart_str
import lxml
import xml.etree.ElementTree as ET
import re
import os
import couchdb


class Invoice:
    def __init__(self):

        self.tagname = []
        self.tagcontent = []
        self.final_dict = {}
        self.flag = 0

    #
    # Reads the XML and returns a list key | value e.g.: Tag -> Content
    #
    def readXML(self, root):
        for item in root.iter():
            self.tagname.append(str(item.tag).lower())
            self.tagcontent.append(str(item.text).lower())

        newdict = dict(zip(self.tagname, self.tagcontent))

        return newdict

    #
    # Cleans the JSON of any white space, special characters, or none values
    #
    def cleanJSON(self, tobecleaned):

        '''          JSON CLEANING                '''
        decoded = json.loads(tobecleaned)
        band = 0
        for element in list(decoded):
            if band == 0:
                match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  str(element))
                if (match and band == 0):
                    try:
                        decoded.pop(element)
                        band += 1
                    except Exception as e:
                        print(e)

            if band == 0:
                match = re.match(r'\s+', str(decoded[element]))
                if (match):
                    if element in decoded:
                        try:
                            decoded.pop(element)
                            band += 1
                        except Exception as e:
                            pass

            if band == 0:
                match = re.match(r'ds:signature+', str(element))
                if (match):
                    try:
                        decoded.pop(element)
                        band += 1
                    except Exception as e:
                        pass

            # Clean out none values
            if band == 0:
                match = re.match(r'none+', str(element))
                if (match):
                    try:
                        decoded.pop(element)
                        band += 1
                    except Exception as e:
                        pass

            band = 0

        for i in list(decoded['comprobante']['factura']):
            match = re.search(r'ds:signature+', str(i))
            if (match):
                try:
                    decoded['comprobante']['factura'].pop(i)
                    break
                except Exception as e:
                    print(e)

        for final in list(decoded):
            try:
                if final == "comprobante":
                    decoded = json.dumps(decoded['comprobante'])
                    break
            except:
                pass

        return decoded


class Files:
    def __init__(self):
        self.listFiles = {}
        global path, parser, invoice, db, new_filename
        path = "C:\\Users\\Esteban.Flores\\Documents\\GitHub\\Invoices\\facturas"

        db = self.DBconnect()
        invoice = Invoice()
        new_filename = ""

        self.ReadXmlFiles()

    #
    # DB connection
    #
    def DBconnect(self):
        # '''=========CouchDB'=========='''
        # server = couchdb.Server('http://localhost:5984/')  # ('http://115.146.93.184:5984/')
        client = MongoClient()
        db = client.primer

        try:
            db = client.primer

        except:
            db = client['primer']
        return db

    #
    # Read all the files in the specified folder
    #
    def ReadXmlFiles(self):
        # Open a file
        dirs = os.listdir(path)
        # Rename the files to a conventional name
        for file in list(dirs):
            try:
                new_filename = "INV_" + str(uuid.uuid4()) + ".xml"
                os.rename(os.path.join(path, file), os.path.join(path, new_filename))
                self.processFile(new_filename)
            except:
                print("There was a problem renaming file: " + "\n")

    def processFile(self, file):
        try:
            parser = ET.XMLParser(encoding="UTF-8")
            tree = ET.parse(os.path.join(path, file), parser)
            root = tree.getroot()

            initial_xml = invoice.readXML(root)

            for key, value in initial_xml.items():
                match = re.search(r'xml+', str(value))
                if match:
                    try:
                        initial_xml[key] = xmltodict.parse(smart_str(value).strip())
                        break
                    except Exception as e:
                        print("Problem in the inner xml")

            ini_json = json.dumps(initial_xml)

            final_json = invoice.cleanJSON(ini_json)

            if self.on_data(final_json) == True:
                print(file, "has been processed and saved\n")

            else:
                print(file, "could not be saved, file already exists\n")

        except Exception as e:
            print("There was a problem reading file: ", file)

    # Insert record (xml transform to json) in the db
    def on_data(self, data):
        finaldoc = json.loads(data)

        try:
            id = smart_str(finaldoc['factura']['infotributaria']['claveacceso'])
            finaldoc["_id"] = id[-10:]
            db.primer.insert_one(finaldoc)
            status = True

        except Exception as e:
            status = False

        return status


A = Files()
