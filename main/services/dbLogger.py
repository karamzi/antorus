import logging

from django.db import connection

class DbLogging(logging.Handler):
    def emit(self, record):
        message = self.format(record)

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO main_logsmodel (message, time) VALUES (%s, CURRENT_TIMESTAMP)", [message])

