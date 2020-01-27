from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from config.logger import logger
from config.config import Config
from routes.general import General
from routes.task import Task
from routes.tasks.completeTask import CompleteTask
from routine import Routine


def main():
    logger.info('Initialize Zac')
    config = Config()
    general = General()
    task = Task()
    complete_tasks = CompleteTask()

    updater = Updater(config.get_token_bot(), use_context=True)
    dp = updater.dispatcher

    routine = Routine(updater.bot)
    routine.start(60)

    dp.add_handler(CommandHandler("start", general.start))
    dp.add_handler(CallbackQueryHandler(complete_tasks.completeTask))
    dp.add_handler(CommandHandler("completeTask",
                   complete_tasks.tasks))

    dp.add_handler(task.get_conv_handler())

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
