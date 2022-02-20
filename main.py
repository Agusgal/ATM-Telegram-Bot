from TelegramBot import TelegramBot
import config


myBot = TelegramBot(token=config.access_token )

if __name__ == '__main__':
    myBot.start_polling()
