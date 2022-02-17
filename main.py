import logging
import os
from TelegramBot import TelegramBot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


myBot = TelegramBot(token=os.environ['TOKEN'])

if __name__ == '__main__':
    myBot.start_polling()
