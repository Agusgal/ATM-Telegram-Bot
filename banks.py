import json


def getBankData():
    """
    Devuelve data de cajeros que recibieron extracciones y estan en la bsae de datos

    Retorna:
    ---------
    disctionary: dict
        diccionario con data parseada del json que almacena la informacion con los cajeros que tuvieron extracciones
    """
    with open('banks.json', 'r') as fp:
        dictionary = json.load(fp)
    return dictionary


def loadBankData(data):
    """
    Carga data a la abse de datos de cajeros

    Parametros:
    ------------
    data: dict
        Diccionario con data a cargar
    """
    with open('banks.json', 'w') as fp:
        json.dump(data, fp)


