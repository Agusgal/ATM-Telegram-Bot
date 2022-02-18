from telegram.ext import Updater, CommandHandler, PrefixHandler, MessageHandler,Filters, CallbackContext
from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from search import bsearch
from data import Data
from map import createMap
import geopy.distance
import numpy as np


class TelegramBot:

    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.add_Dispatchers()

        self.bank = None
        self.location = None
        self.data = None
        self.tolerance = 0.004522
        self.nearestATMs = []

    def add_Dispatchers(self):
        startHandler = CommandHandler('start', self.startCb)
        self.dispatcher.add_handler(startHandler)

        helpHandler = PrefixHandler('', 'help', self.helpCb)
        self.dispatcher.add_handler(helpHandler)

        bankHandler = PrefixHandler('', ['Link', 'link', 'Banelco', 'banelco'], self.bankCb)
        self.dispatcher.add_handler(bankHandler)

        locationHandler = MessageHandler(Filters.location, self.locationCb)
        self.dispatcher.add_handler(locationHandler)

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def startCb(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Hola! soy el BsAs ATM bot a tu servicio!\nPara ver una lista con los comandos utilizá el comando 'help'")

    def helpCb(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='<b>Comandos disponibles: </b> \nLink - muestra cajeros de red Link más cercanos \nBanelco - muestra cajeros de red Banelco más cercanos ',
                                 parse_mode=ParseMode.HTML)

    def bankCb(self, update: Update, context: CallbackContext):
        buttons = [[KeyboardButton(text='Share your location', request_location=True)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text='Voy a necesitar saber tu ubicación:',
                                 reply_markup=ReplyKeyboardMarkup(buttons))
        self.bank = update.message.text

    def locationCb(self, update: Update, context: CallbackContext):
        self.location = update.message.location
        selectedATMS = self.searchbanks()

        for atm in selectedATMS:
            index = np.where(self.data.array == atm[0])
            self.nearestATMs.append(self.data.array[index[0]])

        msg = 'Se encontraron {}'.format(len(self.nearestATMs)) + ' cajeros cerca tuyo:\n\n'
        for atm in self.nearestATMs:
            msg += '<b>{}</b>'.format(atm[0][3]) + '\n'
            msg += 'Dirección: {}'.format(atm[0][5]) + '\n'

        context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=ParseMode.HTML)

        if len(self.nearestATMs):
            self.generateMap()
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('map.png', 'rb'))

    def searchbanks(self):
        self.loadbanks()
        sortd = self.data.getSortedArray(2)

        #ubicacion = (-34.591709, -58.411303)

        #hi = bsearch(sortd, -34.591709 + self.tolerance)
        #lo = bsearch(sortd, -34.591709 - self.tolerance, low=hi)

        hi = bsearch(sortd, self.location.latitude + self.tolerance)
        lo = bsearch(sortd, self.location.latitude - self.tolerance, low=hi)

        atms = []
        for atm in sortd[hi:lo]:
            cajero = (atm[2], atm[1])
            #distance = geopy.distance.distance((-34.591709, -58.411303), cajero).km
            distance = geopy.distance.distance((self.location.latitude, self.location.longitude), cajero).km
            if distance < 0.5:
                atms.append([atm[0], distance])

        if len(atms) > 3:
            sorted(atms, key=lambda x: x[1])
            while len(atms) > 3:
                atms.pop()

        return atms

    def loadbanks(self):
        self.data = Data('cajeros-automaticos.csv', indexfilter=self.bank.upper())

    def generateMap(self):
        points = []
        for atm in self.nearestATMs:
            points.append([float(atm[0][2]), float(atm[0][1])])

        createMap(self.location.latitude, self.location.longitude, points)