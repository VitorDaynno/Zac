from redis import Redis

from config.logger import logger
from config.config import Config


class RedisHelper:

    def __init__(self):
        logger.info("Starting RedisHelper")
        config = Config()
        self.__host = config.get_redis_server()
        self.__port = config.get_redis_port()
        self.__db = config.get_redis_db()
        self.__redis = None

    def __open(self):
        try:
            logger.info("Starting open connect to Redis")
            host = self.__host
            port = self.__port
            db = self.__db
            self.__redis = Redis(host, port, db)
        except Exception as error:
            logger.error("An error occurred {0}".format(error))

    def set_value(self, key, value):
        try:
            logger.info("Setting value by key {0}".format(key))
            self.__open()
            self.__redis.set(key, value)
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def get_value(self, key):
        try:
            logger.info("Getting value by key {0}".format(key))
            self.__open()
            value = self.__redis.get(key)
            return value
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))

    def delete_key(self, key):
        try:
            logger.info("Removing item by key {0}".format(key))
            self.__open()
            value = self.__redis.delete(key)
            return value
        except Exception as error:
            logger.error("An error occurred: {0}".format(error))
