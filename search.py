import numpy as np


def bsearch(arr: np.array, limit, low=0, high=None, key=None):

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


#Performance test
"""
#import time
#import geopy.distance
#from data import Data

customData = Data('cajeros-automaticos.csv', indexfilter='LINK')
ubicacion = (-34.591709, -58.411303)


tol = 0.004522
lat = -34.591709

start4 = time.time()
start1 = time.time()

ordenadoLink = customData.getSortedArray(2)
end1 = time.time()

start2 = time.time()
indiceHigh = bsearch(ordenadoLink, lat + tol)
indiceLow = bsearch(ordenadoLink, lat - tol, low=indiceHigh)
end2 = time.time()
#Ahora tengo los limites entre cuales buscar

start3 = time.time()

ids = []
for atm in ordenadoLink[indiceHigh:indiceLow]:
    cajero = (atm[2], atm[1])
    if geopy.distance.distance(ubicacion, cajero).km < 0.5:
        ids.append(atm[0])
end3 = time.time()
end4 = time.time()

print("Tiempo de ordenamiento de arreglos: ",(end1-start1),"sec")
print("Tiempo de busqueda binaria de indices: ",(end2-start2),"sec")
print("Tiempo de busqueda secuencial limitada: ",(end3-start3),"sec")
print("Tiempo total: ",(end4-start4),"sec")
"""


