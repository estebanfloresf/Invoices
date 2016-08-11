import csv

import collections
import pandas as pd
import re

import time

start_time = time.time()
df = pd.DataFrame()
e = {'impuesto_valor_4': '1.07', 'cantidad_4': '1', 'impuesto_valor_3': '0.17', 'precio_sin_impuesto_5': '7.19',
     'descripcion_3': 'aguagas botella', 'impuesto_valor_5': '0.86', 'impuesto_valor_6': '0.69',
     'impuesto_valor_0': '0.21', 'impuesto_valor_1': '0.21', 'precio_sin_impuesto_2': '1.76',
     'fechaemision': '14/02/2016', 'cantidad_1': '1', 'precio_sin_impuesto_4': '8.9', 'precio_sin_impuesto_3': '1.41',
     'razonsocial': 'aserlaco s.a', 'impuesto_valor_2': '0.21', 'descripcion_4': 'ensalada thai',
     'precio_sin_impuesto_6': '5.79', 'cantidad_6': '1', 'cantidad_0': '1', 'descripcion_2': 'limonada-coco',
     'descripcion_6': 'ensal. barra', 'descripcion_5': 'crp.pechu pavo ques', 'cantidad_3': '1', 'cantidad_2': '1',
     'descripcion_1': 'limonada-coco', 'cantidad_5': '1', 'descripcion_0': 'limonada-coco',
     'precio_sin_impuesto_1': '1.76', 'precio_sin_impuesto_0': '1.76'}

# e = {'impuesto_valor': '1.07',
#      'cantidad': '1',
#      'precio_sin_impuesto': '7.19',
#      'descripcion': 'aguagas botella',
#      'fechaemision': '14/02/2016',
#      'razonsocial': 'aserlaco s.a', }

i = 0
listfinal = []
rsocial = ""
fecha = ""
band=0
while i <= len(e):
    list = ['', '', '', '']

    for key, value in e.items():
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
                    list[0] = value
                    continue
                if cantidad:
                    list[1] = value
                    continue
                if impvalor:
                    list[2] = value
                    continue
                if psinimp:
                    list[3] = value
                    continue

        except:
                if razonsocial:
                    rsocial = str(value)
                    band +=1
                    continue
                if fech:
                    fecha = str(value)
                    band += 1
                    continue

                if desc:
                    list[0] = value
                    i+=1
                    continue
                if cantidad:
                    list[1] = value
                    i+=1
                    continue
                if impvalor:
                    list[2] = value
                    i+=1
                    continue
                if psinimp:
                    list[3] = value
                    i+=1
                    continue


    if list[0]!='':
          list.insert(0,rsocial)
          list.insert(1,fecha)
          listfinal.append(list)

    if band==2 and len(e)==6:
            break


    i+=1

try:
    with open("output.csv", "w") as f:
        fieldnames = [['razonsocial','fecha','descripcion','cantidad','impuesto','valor']]
        writer = csv.writer(f)
        writer.writerows(fieldnames)
        for row in listfinal:
            writer.writerow(row)
except Exception as e: print("The file is open, cannot generate new one")

# print(listfinal)
print("File generated in: %s seconds" % (time.time() - start_time))
