import threading
from datetime import datetime
from helpers.threadJob import ThreadJob

from controllers.task import TaskController
from controllers.user import UserController


class Routine:

    def __init__(self, bot):
        self.event = threading.Event()
        self.bot = bot

    def start(self, time):
        routine = ThreadJob(self.rememberTask, self.event, time)
        routine.start()

    def start_routine(self, function, time):
        routine = ThreadJob(function, self.event, time)
        routine.start()

    def rememberTask(self):
        user_controller = UserController(None)
        users = user_controller.get_users()
        for user in users:
            task_controller = TaskController(user['chat_id'])
            now = datetime.utcnow()
            initial_date = datetime(now.year, now.month, now.day, now.hour,
                                    now.minute, 0)
            minute = now.minute
            if minute < 59:
                minute = minute + 1
            final_date = datetime(now.year, now.month, now.day, now.hour,
                                  minute)
            search_filter = {"date": {"$gte": initial_date, "$lt": final_date}}
            tasks = task_controller.get_tasks(search_filter)
            for task in tasks:
                self.bot.send_message(user["chat_id"], 'Está na hora de ' +
                                      task["name"])
            task_controller.close_connection()
        user_controller.close_connection()
