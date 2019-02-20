from datetime import datetime, timedelta
from pytz import timezone
import pytz


class TaskController:

    def __init__(self, usu_id):
        self._usu_id = usu_id

    def save_task(self, task):
        self.task = {}
        self.task["name"] = task["name"]

        date = task["date"].split('/')
        hour = task["hour"].split(":")
        new_date = datetime(int(date[2]), int(date[1]), int(date[0]),
                            int(hour[0]), int(hour[1]), int(hour[2]))

        self.task['date'] = self._to_UTC(new_date)

    def get_usu_id(self):
        return self._usu_id

    def get_tasks(self, filter):
        filters = {'usuId': self._usu_id}
        if 'date' in filter:
            filters["date"] = filter["date"]
        return self._dao.get_tasks(filters)

    def _to_UTC(self, date):
        tz = timezone('America/Sao_Paulo')
        return tz.normalize(tz.localize(date)).astimezone(pytz.utc)

    def close_connection(self):
        self._dao.close_connection()
