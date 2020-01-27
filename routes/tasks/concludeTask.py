from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

from config.logger import logger
from controllers.task import TaskController


class ConcludeTask:

    @classmethod
    def tasks(self, update, context):
        try:
            logger.info('initiating /concludeTasks')

            chat_id = update.message.chat.id
            taskController = TaskController(chat_id)
            now = datetime.utcnow()
            initial_date = datetime(now.year, now.month, now.day, 0, 0, 0)
            final_date = datetime(now.year, now.month, now.day, 23, 59, 59)
            search_filter = {
                "date": {
                    "$gte": initial_date,
                    "$lt": final_date
                },
                "isConclude": False
            }
            tasks = taskController.get_tasks(search_filter)
            keyboard = []

            if len(list(tasks)) > 0:
                for task in tasks:
                    task_id = str(task["_id"])
                    name = task["name"]
                    response = task_id + ";" + name
                    line = InlineKeyboardButton(name, callback_data=response)
                    keyboard.append([line])
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Qual tarefa deseja concluir?',
                                          reply_markup=reply_markup)
            else:
                update.message.reply_text(
                    "Não existem tarefas a serem concluídas")
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    @classmethod
    def conclude_task(self, update, context):
        try:
            task_controller = TaskController(None)
            query = update.callback_query
            data = query.data
            task_id, name = data.split(";")
            task_controller.conclude_task(task_id)
            query.edit_message_text(
                text="{0} concluída com sucesso".format(name)
            )
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
