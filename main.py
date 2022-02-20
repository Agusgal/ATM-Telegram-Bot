import logging
import os
from TelegramBot import TelegramBot
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


myBot = TelegramBot(token=config.access_token )

if __name__ == '__main__':
    myBot.start_polling()
