from telegram.ext import (Updater, CommandHandler)

from config.logger import logger
from config.config import Config
from routes.general import General


def main():
    logger.info('Initialize Zac')
    config = Config()
    general = General()

    updater = Updater(config.get_token_bot())
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", general.start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
