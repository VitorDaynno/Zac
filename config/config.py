import os
from config.logger import logger


class Config:

    def __init__(self):
        logger.info('Initializing configs')
        self._token_bot = os.getenv('TOKEN_BOT')
        try:
            logger.info('Token bot getting by environment variable: ' + self._token_bot)
        except:
            logger.error('TOKEN_BOT is not found')
        self._db_name = 'zac'

    def get_token_bot(self):
        return self._token_bot

    def get_db_name(self):
        return self._db_name
