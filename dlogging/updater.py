import os
import pymongo
from check_file_free import _file_path, _logger_check_file_free
from config import mongo_config as config
from datetime import datetime
import time

_COLLECTION_NAME = "dlogging"


class DAL(object):
    def __init__(self):
        self._client = None
        self._db = None
        self._collection = None

    def connect(self):
        connection_params = {k: config[k] for k in ["host", "port"]}
        db_name = config["db"]
        self._client = pymongo.MongoClient(**connection_params)
        self._db = self._client[db_name]
        self._collection = self._db[_COLLECTION_NAME]

    def _ensure_indexes(self):
        datetime_idx = pymongo.IndexModel([("time", pymongo.ASCENDING)])
        source_idx = pymongo.IndexModel([("source", pymongo.ASCENDING)])
        level_idx = pymongo.IndexModel([("level", pymongo.ASCENDING)])
        self._collection.create_indexes([datetime_idx, source_idx, level_idx])

    def insert_many(self, docs):
        self._collection.insert_many(docs)



def parse_line(line):
    parts = line.split("#")
    return {
        "time": datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S.%f"),
        "source": parts[1],
        "level": parts[2],
        "message": parts[3]

    }


if __name__ == "__main__":
    dal = DAL()
    dal.connect()

    while True:
        if os.path.exists(_file_path):
            cur_docs = []
            with open(_file_path, "r") as fdr:
                for line in fdr:
                    doc = parse_line(line)
                    cur_docs.append(doc)
            os.remove(_file_path)
            dal.insert_many(cur_docs)
        time.sleep(30)




