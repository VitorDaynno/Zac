from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config.logger import logger
from controllers.task import TaskController
from helpers.dateHelper import DateHelper


class ConcludeTask:

    def __init__(self):
        self.__date_helper = DateHelper()

    def tasks(self, update, context):
        try:
            logger.info('initiating /concludeTasks')

            chat_id = update.message.chat.id
            taskController = TaskController(chat_id, None)
            initial_date = self.__date_helper.initial_date()
            final_date = self.__date_helper.final_date()
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
                    response = "concludeTasks" + "§" + task_id
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
            task_controller = TaskController(None, None)
            query = update.callback_query
            data = query.data

            callback = data.split("§")

            task_id = callback[1]

            task_controller.conclude_task(task_id)
            query.edit_message_text(
                text="Tarefa concluída com sucesso"
            )
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
