from config.logger import logger
from controllers.user import UserController


class General:

    def start(self, bot, update):
        logger.info('initiating /start')

        chat_id = update.message.chat.id
        name = update.message.chat.first_name
        reply = update.message

        user = UserController(chat_id)
        user.set_name(name)
        r = user.new_user(user)

        if r:
            reply.reply_text('Oi ' + user.get_name() + '.')
            reply.reply_text(('Meu nome é Zac, sou um bot com a função de '
                              'ajudar a se lembrar de realizar suas tarefas'))
            reply.reply_text(('Você pode iniciar uma nova tarefa utilizando '
                              'o comando /newTask'))
        else:
            reply.reply_text('A gente já se conhece kekeke')
