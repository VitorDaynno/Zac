import os
from config.logger import logger


class Config:

    def __init__(self):
        logger.info("Initializing configs")

    def get_token_bot(self):
        try:
            self.__token_bot = os.getenv("TOKEN_BOT")
            if self.__token_bot is None:
                raise Exception("TOKEN_BOT is not found")
            logger.info("Token bot getting by environment variable")
            return self.__token_bot
        except Exception as error:
            logger.error("An error occurred {0}".format(error))

    def get_db_name(self):
        logger.info("Getting db name by config")
        self.__db_name = os.getenv("DB_NAME")
        if self.__db_name is None:
            self.__db_name = "zac"
        return self.__db_name

    def get_db_server(self):
        logger.info("Getting db server by config")
        self.__db_server = os.getenv("DB_SERVER")
        if self.__db_server is None:
            self.__db_server = "localhost"
        return self.__db_server

    def get_redis_server(self):
        logger.info("Getting redis server by config")
        REDIS_SERVER = os.getenv("REDIS_SERVER")
        if REDIS_SERVER is None:
            REDIS_SERVER = "localhost"
        return REDIS_SERVER

    def get_redis_port(self):
        logger.info("Getting redis port by config")
        REDIS_PORT = os.getenv("REDIS_PORT")
        if REDIS_PORT is None:
            REDIS_PORT = 6379
        return REDIS_PORT

    def get_redis_db(self):
        logger.info("Getting redis db by config")
        REDIS_DB = os.getenv("REDIS_DB")
        if REDIS_DB is None:
            REDIS_DB = 0
        return REDIS_DB
