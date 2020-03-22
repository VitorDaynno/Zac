from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from datetime import date, timedelta

from config.logger import logger

NAME, DATE, HOUR, BIO = range(4)


class NewTask:

    def __init__(self, TaskController):
        self.TaskController = TaskController
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newTask', self.new_task)],
            states={
                NAME: [MessageHandler(Filters.text, self.name)],
                DATE: [MessageHandler(Filters.text, self.date)],
                HOUR: [MessageHandler(Filters.text, self.hour)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    @classmethod
    def new_task(self, update, context):
        logger.info("Initialize a new task")
        update.message.reply_text('Opa! Uma nova tarefa, qual o nome dela?')

        return NAME

    def name(self, update, context):
        logger.info("Getting task's name")

        chat_id = update.message.chat.id
        name = update.message.text

        if len(name) > 0:
            task_controller = self.TaskController(chat_id)
            task_controller.set_name(name)

            update.message.reply_text('E qual seria o dia?')

            return DATE

        update.message.reply_text('Você tem certeza que digitou um nome?')

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
        self.task = {}
        update.message.reply_text("Sua tarefa foi cancelada :(")

        return ConversationHandler.END

    def get_conv_handler(self):
        return self.conv_handler
