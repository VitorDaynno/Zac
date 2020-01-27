from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from config.logger import logger
from config.config import Config
from routes.general import General
from routes.task import Task
from routes.tasks.concludeTask import ConcludeTask
from routine import Routine


def main():
    logger.info('Initialize Zac')
    config = Config()
    general = General()
    task = Task()
    conclude_task = ConcludeTask()

    updater = Updater(config.get_token_bot(), use_context=True)
    dp = updater.dispatcher

    routine = Routine(updater.bot)
    routine.start(60)

    dp.add_handler(CommandHandler("start", general.start))
    dp.add_handler(CallbackQueryHandler(conclude_task.conclude_task))
    dp.add_handler(CommandHandler("concludeTask", conclude_task.tasks))

    dp.add_handler(task.get_conv_handler())

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
