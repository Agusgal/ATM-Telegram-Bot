import csv
import numpy as np


class Data:
    """
    Clase utilizada para guardar informacion leida directo del archivo csv de bancos, simula dataframe de pandas.

    Atributos:
    -----------
    header: np.array
        arreglo numpy con las categorias de cada dato de los cajeros
    array: np.array
        arreglo numpy con datos de cada cajero

    Metodos:
    ---------
    parsefile(filename, indexfilter=None)
        abre y parsea aarchivo a los atributos de la clase, con indexfilter se puede filtrar segun alguna categoria,
        por ejemplo 'link' solo guarda cajeros que tengan la etiqueta link, evitando guardar datos innecesarios.
    getSortedArray(column)
        devuelve arreglo ordenado segun alguna columna
    """

    def __init__(self, filename, indexfilter=None):
        """
        Parametros:
        -----------
        filename: str
            nombre del archivo que se quiere abrir
        indexfilter: str
            filtro para abrir archivo
        """

        self.header, self.array = self.parseFile(filename, indexfilter)

    def parseFile(self, filename, indexfilter=None):
        """
        Parsea archivo y puede filtrarse segun alguna categoria del archivo csv, por defecto parsea el archivo completo

        Parametros:
        -----------
        filename: str
            nombre del archivo (path)
        indexfilter: str
            categria de filtrado

        Retorna:
        header: np.array
            arreglo numpy con categorias de archivo
        array: np.array
            arreglo con datos de cada cajero
        """

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
        """
        Retorna arreglo ordenado segun una columna

        Parametros:
        ------------
        column: int
            indice de columan segun se quiere reordenar el arreglo
        """
        return self.array[self.array[:, column].argsort()]


#Performance test
"""
import geopy.distance
import time

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

