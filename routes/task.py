from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from datetime import date, timedelta

from config.logger import logger
from controllers.task import TaskController

NAME, DATE, HOUR, BIO = range(4)


class Task:

    def __init__(self):
        self.task = {}
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newTask', self.new_task)],
            states={
                NAME: [MessageHandler(Filters.text, self._name)],
                DATE: [MessageHandler(Filters.text, self._date)],
                HOUR: [MessageHandler(Filters.text, self._hour)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def new_task(self, update, context):
        logger.info("Initialize a new task")
        update.message.reply_text('Opa! Uma nova tarefa, qual o nome dela?')

        return NAME

    def _name(self, update, context):
        logger.info("Getting task's name")
        self.task["name"] = update.message.text
        update.message.reply_text('E qual seria o dia?')

        return DATE

    def _date(self, update, context):
        logger.info("Getting task's date")
        task_date = update.message.text.lower().replace('ã', 'a')
        if "hoje" in task_date:
            task_date = date.today()
            task_date = task_date.strftime("%d/%m/%Y")
        elif "amanha" in task_date:
            task_date = date.today() + timedelta(days=1)
            task_date = task_date.strftime("%d/%m/%Y")
        self.task["date"] = task_date
        update.message.reply_text('Em qual horário?')

        return HOUR

    def _hour(self, update, context):
        logger.info("Getting task's hour")
        self.task["hour"] = update.message.text

        chat_id = update.message.chat.id

        task = TaskController(chat_id)
        task.save_task(self.task)
        update.message.reply_text("Uhu!! A tarefa foi criada")

        return ConversationHandler.END

    def cancel(self, update, context):
        logger.info("Cancelling the task")
        update.message.reply_text("Sua tarefa foi cancelada :(")

        return ConversationHandler.END

    def get_conv_handler(self):
        return self.conv_handler
