from telegram.ext import Updater, CommandHandler

from config.logger import logger
from config.config import Config

from controllers.routine import RoutineController
from controllers.task import TaskController

from helpers.dateHelper import DateHelper
from routes.general import General
from routes.task import Task
from routes.tasks.concludeTask import ConcludeTask
from routes.routines.createRoutine import CreateRoutine
from routine import Routine
from routes import set_routes


def create_tasks():
    logger.info("Starting creating tasks by routines")
    routine_controller = RoutineController(None)
    date_helper = DateHelper()

    today = date_helper.initial_date()
    day_of_week = today.weekday()

    search_filter = {
        "$or": [
            {
                "lastCreatedDate": {
                    "$lt": today
                }
            },
            {
                "lastCreatedDate": {
                    "$exists": False
                }
            }
        ],
        "isActive": True,
        "isEnabled": True
    }

    routines = routine_controller.get_routines(search_filter)

    for routine in routines:
        try:
            task_controller = TaskController(routine["userId"])
            now = date_helper.get_now()

            if day_of_week in routine["days"]:
                routine_id = routine["_id"]
                task = {}

                task["name"] = routine["name"]
                task["date"] = date_helper.to_str_date(today)
                task["hour"] = routine["hour"]

                task_controller.save_task(task)

                routine_controller.update_last_created_date(routine_id, now)
                routine_controller.close_connection()
        except Exception as error:
            logger.info("An error occurred: {0}".format(error))


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

    create_tasks_routine = Routine(None)
    create_tasks_routine.start_routine(create_tasks, 60)

    dp.add_handler(CommandHandler("start", general.start))
    dp.add_handler(CommandHandler("concludeTask", conclude_task.tasks))
    set_routes(dp)

    dp.add_handler(task.get_conv_handler())
    dp.add_handler(create_routine.get_conv_handler())

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
