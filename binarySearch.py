def bsearch(arr, limit, low=0, high=None, key=None):

    if low < 0:
        raise ValueError('low must be non-negative')
    if high is None:
        high = len(arr)

    if key is None:
        while low < high:
            mid = (low + high) // 2
            if abs(float(arr[mid][2])) < abs(limit):
                low = mid + 1
            else:
                high = mid
    return low

import csv, time

file = open("cajeros-automaticos.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)

ubicacion = (-34.591709, -58.411303)
import geopy.distance

tol = 0.004522
lat = -34.591709

link = []
banelco = []
for row in csvreader:
    if row[4] == 'BANELCO':
        banelco.append(row)
    else:
        link.append(row)

start4 = time.time()
start1 = time.time()
from operator import itemgetter
ordenadoLink = sorted(link, key=itemgetter(2))
end1 = time.time()

start2 = time.time()
indiceHigh = bsearch(ordenadoLink, lat + tol)
indiceLow = bsearch(ordenadoLink, lat - tol, low=indiceHigh)
end2 = time.time()
#Ahora tengo los limites entre cuales buscar

start3 = time.time()
for atm in ordenadoLink[indiceHigh:indiceLow]:
    cajero = (atm[2], atm[1])
    if geopy.distance.distance(ubicacion, cajero).km < 0.5:
        print('Encontrado!')
        print(atm[3], atm[5], atm[2], atm[1])
end3 = time.time()
end4 = time.time()

print("Tiempo de ordenamiento de arreglos: ",(end1-start1),"sec")
print("Tiempo de busqueda binaria de indices: ",(end2-start2),"sec")
print("Tiempo de busqueda secuencial limitada: ",(end3-start3),"sec")
print("Tiempo total: ",(end4-start4),"sec")



