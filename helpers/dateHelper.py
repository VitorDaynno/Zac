from pytz import timezone
import pytz
from datetime import datetime


class DateHelper:

    @staticmethod
    def to_UTC(date):
        tz = timezone('America/Sao_Paulo')
        return tz.normalize(tz.localize(date)).astimezone(pytz.utc)

    def initial_date(self):
        now = self.get_local_now()
        initial_date = datetime(now.year, now.month, now.day, 0, 0, 0)
        return self.to_UTC(initial_date)

    def final_date(self):
        now = self.get_local_now()
        final_date = datetime(now.year, now.month, now.day, 23, 59, 59)
        return self.to_UTC(final_date)

    @staticmethod
    def to_local_timezone(date):
        local_timezone = timezone('America/Sao_Paulo')
        return local_timezone.fromutc(date)

    def get_local_now(self):
        local_timezone = self.get_timezone()
        local_datetime = datetime.now(local_timezone)
        return local_datetime

    @staticmethod
    def get_timezone():
        return timezone("America/Sao_Paulo")
