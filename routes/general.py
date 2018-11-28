from bot import bot
from controllers.user import UserController
from controllers.flow import FlowController


@bot.message_handler(commands=['start'])
def init(message):
    chat_id = message.from_user.id
    user = UserController(chat_id)
    user.set_name(message.from_user.first_name)

    r = user.new_user(user)
    if r:
        bot.send_message(user.get_id(), 'Oi ' + user.get_name() + '.')
        bot.send_message(user.get_id(), 'Meu nome é Zac, sou um bot com a função de ajudar a se lembrar de realizar suas tarefas')
        bot.send_message(user.get_id(), 'você pode iniciar uma nova tarefa digitando /newTask')
    else:
        bot.send_message(user.get_id(), user.get_name() + ', nós já nos conhecemos, não precisa disso né?! Hehehe')


@bot.message_handler(func=lambda m: True)
def talking(message):
    chat_id = message.from_user.id
    user = UserController(chat_id)
    user.set_name(message.from_user.first_name)

    r = user.get_in_flow()
    if 'inFlow' in r:
        flow = FlowController(r['flow'], message, chat_id)
        r = flow.execute_step()
        if r is True:
                next_step = flow.get_next_step()
                flow.update_step(next_step["nextStatus"])
                bot.send_message(user.get_id(), next_step['phrase'])
        else:
                bot.send_message(user.get_id(), r['message'])
