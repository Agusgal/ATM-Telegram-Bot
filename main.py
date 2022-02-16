import logging
from telegram.ext import Updater

updater = Updater(token='5107194088:AAFjSevb8rRf7n7YKTRbTocmovxKFruxsKs', use_context=True)
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

def temp(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(text='Share your location', request_location=True)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Buenas!', reply_markup=ReplyKeyboardMarkup(buttons))

def locationCb(update: Update, context: CallbackContext):
    location = update.message.location
    print(type(location))


#def start(update: Update, context: CallbackContext):
#    context.bot.sendMessage(chat_id=update.effective_chat.id, text='Soy un bot, habla conmigo!')

#def caps(update: Update, context: CallbackContext):
#    textCaps = ' '.join(context.args).upper()
#    context.bot.send_message(chat_id=update.effective_chat.id, text=textCaps)


startHandler = PrefixHandler('', 'start', startCb)
dispatcher.add_handler(startHandler)

helpHandler = PrefixHandler('', 'help', help)
dispatcher.add_handler(helpHandler)

locationHandler = MessageHandler(Filters.location, locationCb)
dispatcher.add_handler(locationHandler)

#capsHandler = CommandHandler('caps', caps)
#dispatcher.add_handler(capsHandler)



#def echo(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


#echoHandler = MessageHandler(Filters.text & (~Filters.command), echo)
#dispatcher.add_handler(echoHandler)

if __name__ == '__main__':
    updater.start_polling()