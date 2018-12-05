from pymongo import MongoClient
from config.config import Config
from config.logger import logger


class FlowDAO:

    def __init__(self):
        self._config = Config()
        self._client = MongoClient(self._config.get_db_server(), 27017)
        self._db = self._client[self._config.get_db_name()]

    def get_next_step(self, flow_type, status):
        logger.info('[FlowDAO] Getting next step in flow {0} by status {1}'.format(flow_type, status))
        collection = self._db.stages
        r = collection.find_one({"status": status, "flowType": flow_type})
        return r

    def close_connection(self):
        self._client.close()
