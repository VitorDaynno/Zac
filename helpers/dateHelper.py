from pytz import timezone
import pytz


class DateHelper:

    @staticmethod
    def to_UTC(date):
        tz = timezone('America/Sao_Paulo')
        return tz.normalize(tz.localize(date)).astimezone(pytz.utc)
