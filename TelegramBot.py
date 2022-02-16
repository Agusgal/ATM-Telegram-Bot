from telegram.ext import Updater

class TelegramBot:

    def __init__(self, token):
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher

    def add_Dispatchers(self):
        pass

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()