from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler)

from config.logger import logger
from config.config import Config
from routes.general import General
from routes.tasks import Task
import routine

def main():
    logger.info('Initialize Zac')
    config = Config()
    general = General()
    task = Task()

    updater = Updater(config.get_token_bot(), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", general.start))

    dp.add_handler(task.get_conv_handler())

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
