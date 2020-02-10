from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from config.logger import logger
from controllers.task import TaskController

NAME, DAYS, HOUR, BIO = range(4)


class CreateRoutine:

    def __init__(self):
        self.routine = {}
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newRoutine', self.new_routine)],
            states={
                NAME: [MessageHandler(Filters.text, self.__name)],
                DAYS: [MessageHandler(Filters.text, self.__days)],
                HOUR: [MessageHandler(Filters.text, self.__hour)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    @classmethod
    def new_routine(self, update, context):
        logger.info("Initialize a new routine")
        update.message.reply_text('Opa! Uma nova rotina, qual o nome dela?')

        return NAME

    def __name(self, update, context):
        try:
            logger.info("Getting routine's name")
            self.routine["name"] = update.message.text

            days_of_week = [
                {"text": 'DOM', "data": 0},
                {"text": 'SEG', "data": 1},
                {"text": 'TER', "data": 2},
                {"text": 'QUA', "data": 3},
                {"text": 'QUI', "data": 4},
                {"text": 'SEX', "data": 5},
                {"text": 'SAB', "data": 6}
            ]

            reply_markup = self.make_keyboard("createRoutine§", days_of_week)
            update.message.reply_text('Selecione os dias?',
                                      reply_markup=reply_markup)

            return DAYS
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def __days(self, update, context):
        logger.info("Getting task's days")
        update.message.reply_text('Em qual horário?')
        return HOUR

    def __hour(self, update, context):
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
        update.message.reply_text("Sua rotina foi cancelada :(")

        return ConversationHandler.END

    def get_conv_handler(self):
        return self.conv_handler

    def select_day(self, update, context):
        try:
            query = update.callback_query
            clicked = query.data.split("§")[1]
            items = []

            keyboard = query.message.reply_markup.inline_keyboard
            for line in keyboard:
                for day in line:
                    text = day.text
                    data = day.callback_data
                    if data.split("§")[1] == clicked:
                        text = "({0})".format(text)
                    item = {
                        "text": text,
                        "data": data
                    }
                    items.append(item)

            reply_markup = self.make_keyboard("", items)

            query.edit_message_reply_markup(reply_markup=reply_markup)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def make_keyboard(self, prefix, items):
        keyboard = []
        lines = []
        for item in items:
            text, data = item.values()
            callback = prefix + str(data)
            button = InlineKeyboardButton(text, callback_data=callback)
            if len(lines) < 2:
                lines.append(button)
            else:
                keyboard.append(lines)
                lines = []
                lines.append(button)
        if len(lines) != 0:
            keyboard.append(lines)
        keyboard_markup = InlineKeyboardMarkup(keyboard)
        return keyboard_markup
