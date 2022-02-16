import logging
from telegram.ext import Updater
import os

updater = Updater(token=os.environ['TOKEN'], use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from telegram.ext import PrefixHandler

from telegram.ext import CommandHandler


from telegram.ext import MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup


def startCb(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! soy el BsAs ATM bot a tu servicio!\nPara ver una lista con los comandos utilizá el comando 'help'")

def help(update: Update, context:CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='<b>Comandos disponibles: </b> \nLink - muestra cajeros de red Link más cercanos \nBanelco - muestra cajeros de red Banelco más cercanos ', parse_mode=ParseMode.HTML)


def locationCb(update: Update, context: CallbackContext):
    location = update.message.location


def bank(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(text='Share your location', request_location=True)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Voy a necesitar saber tu ubicación:',
                             reply_markup=ReplyKeyboardMarkup(buttons))


startHandler = CommandHandler('start', startCb)
dispatcher.add_handler(startHandler)

helpHandler = PrefixHandler('', 'help', help)
dispatcher.add_handler(helpHandler)

bankHandler = PrefixHandler('', ['Link', 'link', 'Banelco', 'banelco'], bank)
dispatcher.add_handler(bankHandler)

locationHandler = MessageHandler(Filters.location, locationCb)
dispatcher.add_handler(locationHandler)



if __name__ == '__main__':
    updater.start_polling()