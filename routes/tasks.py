# from bot import bot
# from controllers.user import UserController


# @bot.message_handler(commands=['newTask'])
# def new_task(message):
#     chat_id = message.from_user.id
#     user = UserController(chat_id)
#     r = user.enable_flow({'type': 'newTask', 'stage': 0})
#     if r.modified_count > 0:
#         bot.send_message(chat_id, 'Opa! Uma nova tarefa, qual será o nome dela?')
#     user.close_connection()    

from telegram import (ReplyKeyboardRemove)
from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from datetime import datetime, timedelta
from pytz import timezone
import pytz

from config.logger import logger

NAME, DATE, HOUR, BIO = range(4)


class Task:

    def __init__(self):
        self.task = {}
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newTask', self.new_task)],
            states={
                NAME: [MessageHandler(Filters.text, self.name)],
                DATE: [MessageHandler(Filters.text, self.date)],
                HOUR: [MessageHandler(Filters.text, self.hour)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def new_task(self, update, context):
        logger.info("Initialize a new task")
        update.message.reply_text('Opa! Uma nova tarefa, qual será o nome dela?')

        return NAME

    def _name(self, update, context):
        logger.info("Getting task's name")
        self.task["date"] = update.message.text
        update.message.reply_text('E qual seria o dia?')

        return DATE

    def _date(self, update, context):
        logger.info("Getting task's date")
        self.task["date"] = update.message.text
        update.message.reply_text('Em qual horário?')

        return HOUR

    def _hour(self, update, context):
        logger.info("Getting task's hour")
        self.task["hour"] = update.message.text

        self._save_task()
        update.message.reply_text("Uhu!! A tarefa foi criada")

        return ConversationHandler.END

    def _cancel(self, update, context):
        logger.info("Cancelling the task")
        update.message.reply_text("Sua tarefa foi cancelada :(")

        return ConversationHandler.END

    def _to_UTC(self, date):
        tz = timezone('America/Sao_Paulo')
        return tz.normalize(tz.localize(date)).astimezone(pytz.utc)

    def _save_task(self):
        task = {}

        task["name"] = self.task["name"]
        date = self.task["date"].split('/')
        hour = self.task["hour"].split(":")

        new_date = datetime(int(date[2]), int(date[1]), int(date[0]), int(hour[0]), int(hour[1]), int(hour[2]))
        self.task['date'] = self._to_UTC(new_date)

    def get_conv_handler(self):
        return self.conv_handler
