import os
from config.logger import logger


class Config:

    def __init__(self):
        logger.info('Initializing configs')

    def get_token_bot(self):
        try:
            self.__token_bot = os.getenv('TOKEN_BOT')
            if self.__token_bot is None:
                raise Exception("TOKEN_BOT is not found")
            logger.info(('Token bot getting by environment'
                        ' variable: ' + self.__token_bot))
            return self.__token_bot
        except Exception as error:
            logger.error("An error occurred {0}".format(error))

    def get_db_name(self):
        logger.info('Getting db name by config')
        self.__db_name = os.getenv('DB_NAME')
        if self.__db_name is None:
            self.__db_name = 'zac'
        return self.__db_name

    def get_db_server(self):
        logger.info('Getting db server by config')
        self.__db_server = os.getenv('DB_SERVER')
        if self.__db_server is None:
            self.__db_server = 'localhost'
        return self.__db_server
