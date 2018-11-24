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
            exit()

    def get_token_bot(self):
        return self._token_bot
