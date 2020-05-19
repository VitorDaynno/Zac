from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from datetime import date, timedelta

from config.logger import logger

NAME, DATE, HOUR, BIO = range(4)


class NewTask:

    def __init__(self, TaskController, RedisHelper):
        self._TaskController = TaskController
        self._redis_helper = RedisHelper()
        self._conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newTask', self._new_task)],
            states={
                NAME: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    self._name
                )],
                DATE: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    self._date
                )],
                HOUR: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    self._hour
                )]
            },
            fallbacks=[CommandHandler('cancel', self._cancel)]
        )

    @classmethod
    def _new_task(self, update, context):
        logger.info("Initialize a new task")
        update.message.reply_text('Opa! Uma nova tarefa, qual o nome dela?')

        return NAME

    def _name(self, update, context):
        try:
            logger.info("Getting task's name")
            redis_helper = self._redis_helper

            chat_id = update.message.chat.id
            name = update.message.text

            if len(name) > 0:
                task_controller = self._TaskController(chat_id, redis_helper)
                task_controller.set_name(name)

                update.message.reply_text('E qual seria o dia?')

                return DATE

            update.message.reply_text('Você tem certeza que digitou um nome?')
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def _date(self, update, context):
        try:
            logger.info("Getting task's date")
            chat_id = update.message.chat.id
            redis_helper = self._redis_helper

            task_date = update.message.text.lower().replace('ã', 'a')
            if "hoje" in task_date:
                task_date = date.today()
                task_date = task_date.strftime("%d/%m/%Y")
            elif "amanha" in task_date:
                task_date = date.today() + timedelta(days=1)
                task_date = task_date.strftime("%d/%m/%Y")

            task_controller = self._TaskController(chat_id, redis_helper)
            task_controller.set_date(task_date)

            update.message.reply_text('Em qual horário?')

            return HOUR
        except ValueError:
            update.message.reply_text("Essa não me parece uma data correta!")
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            update.message.reply_text("Algo de errado aconteceu :(")
            return self._cancel(update, context)

    def _hour(self, update, context):
        try:
            logger.info("Getting task's hour")
            chat_id = update.message.chat.id
            redis_helper = self._redis_helper

            hour = update.message.text

            task = self._TaskController(chat_id, redis_helper)
            task.create_task(hour)
            update.message.reply_text("Uhu!! A tarefa foi criada")

            return ConversationHandler.END
        except ValueError:
            update.message.reply_text("Esse não me parece um horário correto!")
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
            update.message.reply_text("Algo de errado aconteceu :(")
            return self._cancel(update, context)

    @classmethod
    def _cancel(self, update, context):
        logger.info("Cancelling the task")
        update.message.reply_text("Sua tarefa foi cancelada :(")

        return ConversationHandler.END

    def get_conv_handler(self):
        return self._conv_handler
