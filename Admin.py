import csv

from pymongo import MongoClient
import flatdict
import pandas as pd




client = MongoClient()
db = client.primer
coll = db.dataset



cursor = db.primer.find({ "factura.infofactura.importetotal": { '$gt': '0' } }, {"factura.infotributaria.nombrecomercial":1,
                                                                                 "factura.infofactura.fechaemision":1 ,
                                                                                 "factura.infofactura.totalsinimpuestos": 1,
                                                                                 "factura.infofactura.totalconimpuestos.totalimpuesto.valor":1,
                                                                                 "factura.infofactura.propina": 1,
                                                                                 "factura.infofactura.importetotal": 1,
                                                                                  "_id": 0
                                                                                 })


with open('dict.csv', 'w') as csv_file:
    fieldnames = ['nombrecomercial', 'fechaemision','totalsinimpuestos','impuesto','propina','total']
    writer = csv.DictWriter(csv_file)
    writer.writerow(fieldnames)
    for document in cursor:
        flat = flatdict.FlatDict(document)
        writer.writerow(flat)


#print(db.primer.count())
