import os
from config.logger import logger


class Config:

    def __init__(self):
        logger.info('Initializing configs')

    def get_token_bot(self):
        self._token_bot = os.getenv('TOKEN_BOT')
        try:
            logger.info(('Token bot getting by environment'
                         ' variable: ' + self._token_bot))
        except:
            logger.error('TOKEN_BOT is not found')
        return self._token_bot

    def get_db_name(self):
        logger.info('Getting db name by config')
        self._db_name = os.getenv('DB_NAME')
        if self._db_name is None:
            self._db_name = 'zac'
        return self._db_name

    def get_db_server(self):
        logger.info('Getting db server by config')
        self._db_server = os.getenv('DB_SERVER')
        if self._db_server is None:
            self._db_server = 'localhost'
        return self._db_server
