from telegram.ext import Updater, CommandHandler

from config.logger import logger
from config.config import Config
from routes.general import General
from routes.task import Task
from routes.tasks.concludeTask import ConcludeTask
from routes.routines.createRoutine import CreateRoutine
from routine import Routine
from routes import set_routes


def main():
    logger.info('Initialize Zac')
    config = Config()
    general = General()
    task = Task()
    create_routine = CreateRoutine()
    conclude_task = ConcludeTask()

    updater = Updater(config.get_token_bot(), use_context=True)
    dp = updater.dispatcher

    routine = Routine(updater.bot)
    routine.start(60)

    dp.add_handler(CommandHandler("start", general.start))
    dp.add_handler(CommandHandler("concludeTask", conclude_task.tasks))
    set_routes(dp)

    dp.add_handler(task.get_conv_handler())
    dp.add_handler(create_routine.get_conv_handler())

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
