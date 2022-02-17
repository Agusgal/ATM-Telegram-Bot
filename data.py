import csv, time
import geopy.distance
import numpy as np


class Data:

    def __init__(self, filename, indexfilter=None):
        self.header, self.array = self.parseFile(filename, indexfilter)

    def parseFile(self, filename, indexfilter=None):
        file = open(filename)
        reader = csv.reader(file)

        header = np.array(next(reader))

        rows = []
        for row in reader:
            if row[4] == indexfilter:
                rows.append(row)
            elif not indexfilter:
                rows.append(row)

        file.close()
        return header, np.array(rows)

    def getSortedArray(self, column):
        return self.array[self.array[:, column].argsort()]


#Performance test
"""
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
"""

