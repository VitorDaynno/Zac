from telegram.ext import CallbackQueryHandler

from src.config.logger import logger
from src.routes.tasks.concludeTask import ConcludeTask
from src.routes.routines.createRoutine import CreateRoutine


def set_routes(bot):
    logger.info('Started set routes')
    bot.add_handler(CallbackQueryHandler(callback_route))


def callback_route(update, context):

    conclude_task = ConcludeTask()
    create_routine = CreateRoutine()

    query = update.callback_query
    data = query.data
    parts = data.split("§")
    callback_route = parts[0]

    if callback_route == "concludeTasks":
        conclude_task.conclude_task(update, context)
    if callback_route == "createRoutine":
        create_routine.select_day(update, context)
