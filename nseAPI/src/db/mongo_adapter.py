from pymongo import MongoClient
from config import Config
from pymodm.connection import connect



class MongoAdapter:
    def __init__(self, conn_string=Config.MONGO_CONNECTION_STRING, db=Config.MONGO_DB):

        # Mongo Connection
        self.db = db
        client_conn_string = conn_string + '?authSource=' + Config.MONGO_AUTH_DB
        self.db_conn_string = conn_string + db + '?authSource=' + Config.MONGO_AUTH_DB
        
        self.__client = MongoClient(client_conn_string)

    def get_mongo_client(self):
        return self.__client

    def get_db(self):
        return self.__client[db]

    def get_connection_string(self):
        return self.db_conn_string

