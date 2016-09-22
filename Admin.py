import csv
import json

import flatdict as flatdict
import re

import time
from pymongo import MongoClient
import flatdict
import pandas as pd


class DatabaseQueries:
    def __init__(self):
        client = MongoClient()
        self.db = client.primer
        coll = self.db.primer

    def renameArray(self):
        cursor = self.db.primer.find({"factura.infofactura.importetotal": {'$gt': '0'}},
                                          {"factura.infotributaria.razonsocial": 1,
                                           "factura.infofactura.fechaemision": 1,
                                           "factura.infofactura.totalsinimpuestos": 1,
                                           "factura.infofactura.totalconimpuestos.totalimpuesto.valor": 1,
                                           "factura.infofactura.propina": 1,
                                           "factura.infofactura.importetotal": 1,
                                           "_id": 0})
        final = []
        for document in cursor:
            flat = flatdict.FlatDict(document)
            for key, value in flat.items():
                try:

                    match = re.search(r'valor+', str(key))
                    if match and value != "0.00":
                        flat["impuesto"] = flat.pop(key)
                        continue

                    match = re.search(r'propina+', str(key))
                    if match:
                        flat["propina"] = flat.pop(key)
                        continue

                    match = re.search(r'razonsocial+', str(key))
                    if match:
                        flat["razonsocial"] = flat.pop(key)
                        continue

                    match = re.search(r'importetotal+', str(key))
                    if match:
                        flat["total"] = flat.pop(key)
                        continue

                    match = re.search(r'fechaemision+', str(key))
                    if match:
                        flat["fechaemision"] = flat.pop(key)
                        continue

                    match = re.search(r'totalsinimpuestos+', str(key))
                    if match:
                        flat["totalsinimpuestos"] = flat.pop(key)
                        continue
                except:
                    print("There was a problem")
            final.append(flat)

        return final

    def invoicestocsv(self):
        df = pd.DataFrame()

        for element in self.renameArray():
            df2 = pd.DataFrame.from_dict(element, orient='index').T
            df2['fechaemision'] = pd.to_datetime(df2['fechaemision'], format="%d/%m/%Y")
            df = df.append(df2, ignore_index=True)

        df = df[['razonsocial', 'fechaemision', 'totalsinimpuestos', 'impuesto', 'propina', 'total']]  # Ordena Columnas

        df.sort_values(by='fechaemision', ascending=True)  # Ordena por fecha factura
        data = df.sort_values(by='fechaemision')
        data.index = range(0, len(data))
        try:
            data.to_csv('C:\\Users\\Esteban.Flores\\Documents\\GitHub\\Invoices\\CSVs\\Invoices.csv', index=True,
                        encoding='UTF-8')
            print("Archivo generado con exito")
        except Exception as e:
            print(e)

    def finalArray(self):
        final =[]
        cursor = self.db.primer.find({"factura.infofactura.importetotal": {'$gt': '0'}},
                                          {"factura.infotributaria.razonsocial": 1,
                                           "factura.infofactura.totalconimpuestos.totalimpuesto.valor": 1,
                                           "factura.infofactura.fechaemision": 1,
                                           "factura.detalles.detalle.preciototalsinimpuesto": 1,
                                           "factura.detalles.detalle.descripcion": 1,
                                           "factura.detalles.detalle.cantidad": 1,
                                           "factura.detalles.detalle.impuestos.impuesto.valor": 1,
                                           "_id": 0})

        for document in cursor:
            flat = flatdict.FlatDict(document)

            for key,value in flat.items():
                try:
                    match = re.search(r'cantidad+', str(key))
                    if match:
                        try:
                            digit = re.search(r'\d+', str(key)).start()
                            if digit:
                                flat["cantidad_"+key[digit]] = flat.pop(key)
                                continue
                        except:
                            flat["cantidad"] = flat.pop(key)
                            continue

                    match = re.search(r'impuesto.valor+', str(key))
                    if match:
                        try:
                            digit = re.search(r'\d+', str(key)).start()
                            if digit:
                                flat["impuesto_valor_" + key[digit]] = flat.pop(key)
                                continue
                        except:
                            flat["impuesto_valor"] = flat.pop(key)
                            continue


                    match = re.search(r'descripcion+', str(key))
                    if match:
                        try:
                            digit = re.search(r'\d+', str(key)).start()
                            if digit:
                                flat["descripcion_" + key[digit]] = flat.pop(key)
                                continue

                        except:
                            flat["descripcion"] = flat.pop(key)
                            continue


                    match = re.search(r'preciototalsinimpuesto+', str(key))
                    if match:
                        try:
                            digit = re.search(r'\d+', str(key)).start()
                            if digit:
                                flat["precio_sin_impuesto_" + key[digit]] = flat.pop(key)
                                continue
                        except:
                            flat["precio_sin_impuesto"] = flat.pop(key)
                            continue

                    match = re.search(r'fechaemision+', str(key))
                    if match:
                        flat["fechaemision"] = flat.pop(key)
                        continue

                    match = re.search(r'razonsocial+', str(key))
                    if match:
                        flat["razonsocial"] = flat.pop(key)
                        continue

                except Exception as e: print(e)
            final.append(flat)
        return final

    def detailsToCSV(self, list):
        start_time = time.time()
        listfinal = []
        for element in list:
            i = 0

            rsocial = ""
            fecha = ""
            band = 0
            while i <= len(element):
                listainicial = ['', '', '', '']

                for key, value in element.items():
                    cantidad = re.search(r'cantidad+', str(key))
                    impvalor = re.search(r'valor+', str(key))
                    psinimp = re.search(r'sin+', str(key))
                    desc = re.search(r'descripcion+', str(key))
                    razonsocial = re.search(r'razonsocial+', str(key))
                    fech = re.search(r'fecha+', str(key))

                    try:
                        digit = re.search(r'\d+', str(key)).start()
                        if int(key[digit]) == i:
                            if desc:
                                listainicial[0] = value
                                continue
                            if cantidad:
                                listainicial[1] = value
                                continue
                            if impvalor:
                                listainicial[2] = value
                                continue
                            if psinimp:
                                listainicial[3] = value
                                continue

                    except:
                        if razonsocial:
                            rsocial = str(value)
                            band += 1
                            continue
                        if fech:
                            fecha = str(value)
                            band += 1
                            continue


                        if desc:
                            listainicial[0] = value
                            i += 1
                            continue
                        if cantidad:
                            listainicial[1] = value
                            i += 1
                            continue
                        if impvalor:
                            listainicial[2] = value
                            i += 1
                            continue
                        if psinimp:
                            listainicial[3] = value
                            i += 1
                            continue

                if listainicial[0] != '':
                    listainicial.insert(0, rsocial)
                    listainicial.insert(1, fecha)
                    listfinal.append(listainicial)

                if band == 2  and len(element) == 6:
                    break

                i += 1

        try:
            with open("C:\\Users\\Esteban.Flores\\Documents\\GitHub\\Invoices\\CSVs\\detail.csv", "w") as f:
                fieldnames = [['razonsocial', 'fecha', 'total','descripcion', 'cantidad', 'impuesto', 'valor']]
                writer = csv.writer(f)
                writer.writerows(fieldnames)
                for row in listfinal:
                    writer.writerow(row)
        except Exception as e:
            print("The file is open, cannot generate new one")

        print("File generated in: %s seconds" % (time.time() - start_time))

    def info(self):
        print("Last document registered by user:")




A = DatabaseQueries()
detalles = A.finalArray()
A.detailsToCSV(detalles)
A.invoicestocsv()
