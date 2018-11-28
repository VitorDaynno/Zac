import threading
import datetime
from helpers.threadJob import ThreadJob
from bot import bot
from controllers.task import TaskController
from controllers.user import UserController

event = threading.Event()


def rememberTask():
    user_controller = UserController(None)
    users = user_controller.get_users()
    for user in users:
        task_controller = TaskController(user['chat_id'])
        now = datetime.datetime.now()
        initial_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)        
        final_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute + 1)
        filter = {"date": {"$gte": initial_date, "$lt": final_date}}
        tasks = task_controller.get_tasks(filter)
        for task in tasks:
            bot.send_message(user["chat_id"], 'Está na hora de ' + task["name"])

routine = ThreadJob(rememberTask, event, 60)
routine.start()
