from bot import bot
from controllers.user import UserController


@bot.message_handler(commands=['newTask'])
def new_task(message):
    chat_id = message.from_user.id
    user = UserController(chat_id)
    r = user.enabled_flow({'flow': 'newTask', 'stage': 0})
    if r.modified_count > 0:
        bot.send_message(chat_id, 'Opa! Uma nova tarefa, qual será o nome dela?')
