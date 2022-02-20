from telegram.ext import Updater, CommandHandler, PrefixHandler, MessageHandler,Filters, CallbackContext
from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from datetime import datetime,timezone
from search import bsearch
from data import Data
from map import createMap
from banks import getBankData, loadBankData
import geopy.distance
import numpy as np

class TelegramBot:
    """
    Clase usada para representar un bot de Telegram

    ...
    Atributos
    ---------------
    updater: telegram.ext.Updater
        Interfaz de la librería Python-Telegram-Bot, contiene información sobre mensajes recibidos
    dispatcher: telegram.ext.Dispatcher
        Interfaz de la librería Python-Telegram-Bot, contiene callbacks a acciones según el tipo de mensajes recibidos
    network: str
        Red de cajeros que el usuario pidió
    location: telegram.Location
        Ubicación de la persona que está madnando mensajes
    datetime: daytime.Daytime
        Horario de consulta a la API de cajeros
    data: data.Data
        Objeto que guarda información sobre los cajeros
    tolerance: int
        Límite de busqueda de cajeros en grados (equivalente a 500 metros en línea recta)
    nearestATMs: list
        Lista con los 3 cajeros más cercanos ya filtrados (está asegurado que los 3 tengan dinero)
    ...
    Métodos
    ---------------
    add_Dispatchers()
        Agrega handlers de callbacks a los dispatchers de los respectivos comandos (tipos de mensajes)
    start_polling()
        Comienza a esperar mensajes (es el loop de funcionamiento de Python-Telegram-Bot)
    startCb(update, context)
        Callback llamado con el comando start
    helpCb(update, context)
        Callback llamado con el comando help
    bankCb(update, context)
        Callback llamado con el comando link o banelco
    locationCb(update, context)
        Callback llamado cuando el usuario envia ubicación
    searchbanks()
        Busca bancos cercanos al usuario
    loadbanks()
        Carga bancos desde la base de datos hacia el objeto correspondiente
    generateMap()
        Genera mapa cercano al usuario
    bankLogic()
        Se encarga de actualizar la base de datos y de conseguir los bancos más cercanos que estén disponibles.
    formatdate()
        Formatea fecha para poder guardarla.
    checkRestock(now, last)
        Chequea que un cajero haya sido repuesto o no.
    """
    def __init__(self, token):
        """
        Parameters
        ----------
        token : str
            token de la API
        """
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.add_Dispatchers()

        self.network = None
        self.location = None
        self.datetime = None
        self.data = None
        self.tolerance = 0.004522
        self.nearestATMs = []

    def add_Dispatchers(self):
        """
        Agrega cada función de callback a su handler corresponiente, se llama en la creación de del objeto Bot.
        """
        startHandler = CommandHandler('start', self.startCb)
        self.dispatcher.add_handler(startHandler)

        helpHandler = PrefixHandler('', 'help', self.helpCb)
        self.dispatcher.add_handler(helpHandler)

        bankHandler = PrefixHandler('', ['Link', 'link', 'Banelco', 'banelco'], self.bankCb)
        self.dispatcher.add_handler(bankHandler)

        locationHandler = MessageHandler(Filters.location, self.locationCb)
        self.dispatcher.add_handler(locationHandler)

    def start_polling(self):
        """
        Llama a updater.start_pollin(), empieza el loop de espera de mensajes.
        """

        self.updater.start_polling()
        self.updater.idle()

    def startCb(self, update: Update, context: CallbackContext):
        """
        Callback llamado con el comando 'start del bot', envia un mensaje de inicio

        Parámetros
        ----------
        update: Update
            updater del Python-Telegram-Bot, contiene información sobre los mensajes, etc
        context: CallbackContext
            contexto del mensaje, contiene al bot, etc
        """
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Hola! soy el BsAs ATM bot a tu servicio!\nPara ver una lista con los comandos utilizá el comando 'help'")

    def helpCb(self, update: Update, context: CallbackContext):
        """
        Callback llamado con el comando help, muestra los comandos disponibles (link y banelco)

        Parámetros
        ----------
        update: Update
            updater del Python-Telegram-Bot, contiene información sobre los mensajes, etc
        context: CallbackContext
            contexto del mensaje, contiene al bot, etc
        """
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='<b>Comandos disponibles: </b> \nLink - muestra cajeros de red Link más cercanos \nBanelco - muestra cajeros de red Banelco más cercanos ',
                                 parse_mode=ParseMode.HTML)

    def bankCb(self, update: Update, context: CallbackContext):
        """
        Callback llamado luego del comando link o banelco, cambia el teclado a un boton de compartir ubicación y actualiza la red bancaria utilizada

        Parámetros
        ----------
        update: Update
            updater del Python-Telegram-Bot, contiene información sobre los mensajes, etc
        context: CallbackContext
            contexto del mensaje, contiene al bot, etc
        """
        buttons = [[KeyboardButton(text='Share your location', request_location=True)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text='Voy a necesitar saber tu ubicación:',
                                 reply_markup=ReplyKeyboardMarkup(buttons))
        self.network = update.message.text

    def locationCb(self, update: Update, context: CallbackContext):
        """
        Callback llamado una vez fue compartida la ubicación, genera los cajeros más cercanos en base a los criterios correspondientes
        y también envía el mensaje con los cajeros encontrados y el mapa de la zona

        Parámetros
        ----------
        update: Update
            updater del Python-Telegram-Bot, contiene información sobre los mensajes, etc
        context: CallbackContext
            contexto del mensaje, contiene al bot, etc
        """
        self.location = update.message.location
        date = update.message.date
        newdate = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        self.datetime = newdate

        #SelectedATMS tiene los bancos cercanos (a menos de 500 metros)
        selectedATMS = self.searchbanks()

        for atm in selectedATMS:
            index = np.where(self.data.array == atm[0])
            newatm = list(self.data.array[index[0]][0])
            newatm.append(atm[1])
            self.nearestATMs.append(newatm)
        self.nearestATMs = sorted(self.nearestATMs, key=lambda l: l[-1], reverse=False)

        #nearestATMs tiene los bancos más cercanos ordenados según su distancia
        self.bankLogic()

        #Luego de banklogic solamente qeudan 3 o menos cajeros
        msg = 'Se encontraron {}'.format(len(self.nearestATMs)) + ' cajeros cerca tuyo:\n\n'
        for atm in self.nearestATMs:
            msg += '<b>{}</b>'.format(atm[3]) + '\n'
            msg += 'Dirección: {}'.format(atm[5]) + '\n'

        context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=ParseMode.HTML)

        if len(self.nearestATMs):
            self.generateMap()
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('map.png', 'rb'))

    def searchbanks(self):
        """
        Busca los bancos más cercanos en un radio de 500 metros, utiliza la funcion bsearch de busqueda binaria para optimizar el proceso.

        Returns:
        --------
        atms: list
            lista de cajeros en un radio de 500 metros del usuario
        """

        #Cargo bancos
        self.loadbanks()
        sortd = self.data.getSortedArray(2)

        #debug
        hi = bsearch(sortd, -34.591709 + self.tolerance)
        lo = bsearch(sortd, -34.591709 - self.tolerance, low=hi)
        #debug

        #hi = bsearch(sortd, self.location.latitude + self.tolerance)
        #lo = bsearch(sortd, self.location.latitude - self.tolerance, low=hi)

        atms = []
        for atm in sortd[hi:lo]:
            cajero = (atm[2], atm[1])

            #debug
            distance = geopy.distance.distance((-34.591709, -58.411303), cajero).km
            #debug

            #distance = geopy.distance.distance((self.location.latitude, self.location.longitude), cajero).km
            if distance < 0.5:
                atms.append([atm[0], distance])

        return atms

    def loadbanks(self):
        """
        Carga bancos en objeto Data
        """
        self.data = Data('cajeros-automaticos.csv', indexfilter=self.network.upper())

    def generateMap(self):
        """
        Crea mapa de zona cercana al usuario utilizando OpenStreetmaps
        """

        points = []
        for atm in self.nearestATMs:
            points.append([float(atm[0][2]), float(atm[0][1])])

        createMap(self.location.latitude, self.location.longitude, points)

    def bankLogic(self):
        """
        Logica de bancos, carga los bancos que tuvieron extracciones recientemente, y chequea que tengan dinero
        basandose en el momento de la ultima extraccion. Ademas de haber mas de 3 cajeros que cumplen los criterios
        se utilizan los 3 mas cercanos y se actualiza la abse de datos.
        """

        tolerance = 100
        bankDict = getBankData()

        nearestATMsCopy = self.nearestATMs.copy()
        for atm in nearestATMsCopy:
            if atm[0] in bankDict['id']:
                index = bankDict['id'].index(atm[0])

                #Chequeo horario ultima extracción
                laststr = bankDict['lastwithdrawal'][index]
                lastwithdrawal = datetime.strptime(laststr, '%d/%m/%y %H:%M')

                #Recargo cajero si se cumplen las condiciones apropiadas.
                if self.checkRestock(self.datetime, lastwithdrawal):
                    bankDict['withdrawals'][index] = 1000

                #Si no hay mas dinero se elimina el cajero
                if (atm[0] in bankDict['id']) and (bankDict['withdrawals'][index] < tolerance):
                    self.nearestATMs.remove(atm)

        if len(self.nearestATMs) > 3:
            self.nearestATMs = self.nearestATMs[:3]

        #Se actualiza la base de datos (diccionario que luego se guarda)
        for atm in self.nearestATMs:
            if atm[0] not in bankDict['id']:
                bankDict['id'].append(atm[0])
                bankDict['withdrawals'].append(1000)
                bankDict['lastwithdrawal'].append(self.formatdate())

        #Actualiza el estimado de recargas restantes
        for ind, atm in enumerate(self.nearestATMs):
            index = bankDict['id'].index(atm[0])
            if len(self.nearestATMs) == 3:
                if not ind:
                    bankDict['withdrawals'][index] -= 0.7
                elif ind == 1:
                    bankDict['withdrawals'][index] -= 0.2
                else:
                    bankDict['withdrawals'][index] -= 0.1
            elif len(self.nearestATMs) == 2:
                if not ind:
                    bankDict['withdrawals'][index] -= 0.7
                else:
                    bankDict['withdrawals'][index] -= 0.3
            elif len(self.nearestATMs) == 1:
                bankDict['withdrawals'][index] -= 1
            bankDict['lastwithdrawal'][index] = self.formatdate()

        #Cargo nueva data al archivo
        loadBankData(bankDict)

    def formatdate(self):
        """
        Crea timestamp formateada para gusardar fecha.
        Retorna:
        ---------
        timestamp:
            data de fecha formateada
        """

        timestamp = self.datetime.strftime('%d/%m/%y %H:%M')
        return timestamp

    def checkRestock(self, now, last):
        """
        Chequea que haya habido un restock de dinero en el cajero entre el tiempo de consulta (now) y la ultima consulta (last)

        Parametros:
        ----------
        now: datetime.Datetime
            objeto datetime con la informacion del horario de la consulta actual a la API.
        last: datetime.Datetime
            objeto datetime con la informacion del horario de la ultima consulta a la API.

        Retorna:
        ----------
        True si hubo recarga, False si no.
        """
        if now.day == last.day:
            if (now.weekday() < 5) and (last.hour < 8) and (now.hour > 8):
                return True
        else:
            if (now.weekday() > 5) and (last.weekday() <= 4) and (last.hour < 8):
                return True
            elif (now.weekday() > 5) and (last.weekday() <= 3):
                return True
            elif (now.weekday() < 5) and (now.hour > 8):
                return True
            elif (now.weekday() < 5) and (last.weekday() < 5) and (now.hour < 8) and (last.hour < 8):
                return True
        return False




