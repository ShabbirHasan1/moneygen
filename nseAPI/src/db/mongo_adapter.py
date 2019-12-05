from pymongo import MongoClient
from config import Config
from pymodm.connection import connect



class MongoAdapter:
    def __init__(self, conn_string=Config.MONGO_CONNECTION_STRING, conn_alias=Config.CONNECTION_ALIAS, db=Config.MONGO_DB):

        # Mongo Connection
        self.__client = MongoClient(conn_string)
        self.db = db
        # PyMODM connection
        connect(conn_string + db, alias=conn_alias)

    def get_mongo_client(self):
        return self.__client

    def get_db(self):
        return self.__client[db]

