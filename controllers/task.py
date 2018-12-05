from daos.taskDAO import TaskDAO
from config.config import Config
import datetime


class TaskController:

    def __init__(self, usu_id):
        self._usu_id = usu_id
        self._dao = TaskDAO()
        self._config = Config()

    def new_task(self, step, text):
        if step == 'name':
            return self._dao.new_task(text, self._usu_id)
        if step == 'date':
            splitText = text.split(' ')
            date = splitText[0].split('/')
            hour = splitText[1].split(':')
            new_date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(hour[0]), int(hour[1]), int(hour[2]))
            return self._dao.update_date(new_date, self._usu_id)

    def disable_in_process(self):
        self._dao.disable_in_process(self._usu_id)

    def get_usu_id(self):
        return self._usu_id

    def get_tasks(self, filter):
        filters = {'usuId': self._usu_id}
        if 'date' in filter:
            filters["date"] = filter["date"]
        return self._dao.get_tasks(filters)
    
    def close_connection(self):
        self._dao.close_connection()
