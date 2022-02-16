import csv, time
import pandas as pd
import geopy.distance

file = open("cajeros-automaticos.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)


rows = []

ubicacion = (-34.591709, -58.411303)

link = []
banelco = []
for row in csvreader:
    if row[4] == 'BANELCO':
        banelco.append(row)
    else:
        link.append(row)

start = time.time()

for atm in link:
    cajero = (atm[2], atm[1])
    if geopy.distance.distance(ubicacion, cajero).km < 0.5:
        print('Encontrado!')
        print(atm[2], atm[1])




end = time.time()

print("Busqueda de cajeros secuencial: ",(end-start),"sec")

file.close()


