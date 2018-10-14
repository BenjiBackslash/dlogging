import pymongo
from config import mongo_config as config

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

    def count(self):
        return self._collection.find({}).count()

    def get(self, level, _from=None):
        filter = {"level": {"$gte":level}}
        if _from is not None:
            filter["time"] = {"$gt": _from}
        return self._collection.find(filter)
