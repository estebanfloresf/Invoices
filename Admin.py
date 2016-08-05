import csv
import json

import flatdict as flatdict
import re
from pymongo import MongoClient
import flatdict
import pandas as pd


class DatabaseQueries:
    def __init__(self):
        client = MongoClient()
        self.db = client.primer
        coll = self.db.dataset



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
            data.to_csv('C:\\Users\\Esteban.Flores\\Documents\\GitHub\\Invoices\\Invoices.csv', index=True,
                        encoding='UTF-8')
            print("Archivo generado con exito")
        except Exception as e:
            print(e)

    def details(self):
        final =[]
        cursor = self.db.primer.find({"factura.infofactura.importetotal": {'$gt': '0'}},
                                          {"factura.infotributaria.razonsocial": 1,
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

    def tocsv(self,list):
        df =pd.DataFrame()
        e = {'impuesto_valor_4': '1.07', 'cantidad_4': '1', 'impuesto_valor_3': '0.17', 'precio_sin_impuesto_5': '7.19', 'descripcion_3': 'aguagas botella', 'impuesto_valor_5': '0.86', 'impuesto_valor_6': '0.69', 'impuesto_valor_0': '0.21', 'impuesto_valor_1': '0.21', 'precio_sin_impuesto_2': '1.76', 'fechaemision': '14/02/2016', 'cantidad_1': '1', 'precio_sin_impuesto_4': '8.9', 'precio_sin_impuesto_3': '1.41', 'razonsocial': 'aserlaco s.a', 'impuesto_valor_2': '0.21', 'descripcion_4': 'ensalada thai', 'precio_sin_impuesto_6': '5.79', 'cantidad_6': '1', 'cantidad_0': '1', 'descripcion_2': 'limonada-coco', 'descripcion_6': 'ensal. barra', 'descripcion_5': 'crp.pechu pavo ques', 'cantidad_3': '1', 'cantidad_2': '1', 'descripcion_1': 'limonada-coco', 'cantidad_5': '1', 'descripcion_0': 'limonada-coco', 'precio_sin_impuesto_1': '1.76', 'precio_sin_impuesto_0': '1.76'}
        i = 0
        listcantidad = []

        for key,value in e.items():
            match = re.search(r'cantidad+', str(key))
            try:
                digit = re.search(r'\d+', str(key)).start()
                if match:
                     listcantidad.insert(int(key[digit]),value)

            except: pass
        print(listcantidad)




        # df = pd.DataFrame.from_dict(e ,orient='index').T
        # df.to_csv('C:\\Users\\Esteban.Flores\\Documents\\GitHub\\Invoices\\facturas\\details.csv', index=True,
        #                  encoding='UTF-8')


        # for element in list:
        #     df2 = pd.DataFrame.from_dict(element, orient='index').T
        #     df2['fechaemision'] = pd.to_datetime(df2['fechaemision'], format="%d/%m/%Y")
        #     df = df.append(df2, ignore_index=True)


        # df = df[indices]  # Ordena Columnas
        # df.sort_values(by='fechaemision', ascending=True)  # Ordena por fecha factura
        # data = df.sort_values(by='fechaemision')
        # data.index = range(0, len(data))
        # try:
        #     data.to_csv('C:\\Users\\Esteban.Flores\\Documents\\GitHub\\Invoices\\facturas\\details.csv', index=True,
        #                 encoding='UTF-8')
        #     print("Archivo generado con exito")
        # except Exception as e:
        #     print(e)



A = DatabaseQueries()
detalles = A.details()
dtlleindices = ['razonsocial', 'fechaemision', 'descripcion', 'impuesto_valor', 'precio_sin_impuesto', 'cantidad']
A.tocsv(detalles)
