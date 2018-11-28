import threading
from helpers.threadJob import ThreadJob
from bot import bot

event = threading.Event()


def foo():
    print("Que tal fazer sua tarefa")

k = ThreadJob(foo, event, 60)
k.start()
