from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from config.logger import logger
from helpers.telegramHelper import TelegramHelper
from controllers.routine import RoutineController

NAME, DAYS, HOUR, BIO = range(4)


class CreateRoutine:

    def __init__(self):
        self.routine = {}
        self.__telegram_helper = TelegramHelper()
        self.__RoutineController = RoutineController
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newRoutine', self.new_routine)],
            states={
                NAME: [MessageHandler(Filters.text, self.__name)],
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

            chat_id = update.message.chat.id
            name = update.message.text

            routine_controller = self.__RoutineController(chat_id)
            routine_controller.set_name(name)

            buttons = [
                {"text": 'DOM', "data": 0},
                {"text": 'SEG', "data": 1},
                {"text": 'TER', "data": 2},
                {"text": 'QUA', "data": 3},
                {"text": 'QUI', "data": 4},
                {"text": 'SEX', "data": 5},
                {"text": 'SAB', "data": 6},
                {"text": "Continuar", "data": "OK"}
            ]

            reply_markup = self.__telegram_helper.make_keyboard(
                "createRoutine§",
                buttons
            )

            update.message.reply_text('Selecione os dias?',
                                      reply_markup=reply_markup)

            return HOUR
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def __hour(self, update, context):
        try:
            logger.info("Getting routine's hour")

            chat_id = update.message.chat.id
            hour = update.message.text

            routine_controller = self.__RoutineController(chat_id)
            routine_controller.set_hour(hour)

            chat_id = update.message.chat.id

            routine = self.__RoutineController(chat_id)
            routine.save_routine(self.routine)

            update.message.reply_text("Uhu!! A rotina foi criada!")

            return ConversationHandler.END
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            if error.args[0] == "Time is invalid":
                update.message.reply_text("Tem certeza que isso é um horário?")
            else:
                update.message.reply_text("Ish, parece que algo deu errado")

    def cancel(self, update, context):
        logger.info("Cancelling the task")
        self.routine = {}
        update.message.reply_text("Sua rotina foi cancelada :(")

        return ConversationHandler.END

    def get_conv_handler(self):
        return self.conv_handler

    def select_day(self, update, context):
        try:
            query = update.callback_query
            clicked = query.data.split("§")[1]

            if clicked == "OK":
                return self.__confirm_days(update)

            items = []

            keyboard = query.message.reply_markup.inline_keyboard
            for line in keyboard:
                for day in line:
                    text = day.text
                    data = day.callback_data
                    if data.split("§")[1] == clicked:
                        if "(" not in text:
                            text = "({0})".format(text)
                        else:
                            text = text.replace("(", "")
                            text = text.replace(")", "")
                    item = {
                        "text": text,
                        "data": data
                    }
                    items.append(item)

            reply_markup = self.__telegram_helper.make_keyboard("", items)

            query.edit_message_reply_markup(reply_markup=reply_markup)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def __confirm_days(self, update):
        logger.info("Started confirm days")

        query = update.callback_query
        message = query.message
        chat_id = message.chat.id
        keyboard = message.reply_markup.inline_keyboard

        days = []
        i = 0

        for line in keyboard:
            for day in line:
                text = day.text
                if "(" in text:
                    days.append(i)
                i += 1

        routine_controller = self.__RoutineController(chat_id)
        routine_controller.set_days(days)

        query.message.reply_text("E qual seria o horário?")
