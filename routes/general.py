from bot import bot
from controllers.user import UserController


@bot.message_handler(commands=['start'])
def init(message):
    chat_id = message.from_user.id
    user = UserController(chat_id)
    user.set_name(message.from_user.first_name)

    r = user.new_user(user)
    if r:
        bot.send_message(user.get_id(), 'Oi ' + user.get_name() + '.')
        bot.send_message(user.get_id(), 'Meu nome é Zac, sou um bot com a função de ajudar a se lembrar de realizar suas tarefas')
        bot.send_message(user.get_id(), 'você pode iniciar uma nova tarefa digitando /newTasks')
    else:
        bot.send_message(user.get_id(), user.get_name() + ', nós já nos conhecemos, não precisa disso né?! Hehehe')