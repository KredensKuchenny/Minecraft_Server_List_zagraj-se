from pymongo import MongoClient
from config.config import database_login
from pymongo.database import Database


MONGODB_CONN = "mongodb://{}:{}@{}:{}/?authSource={}".format(
    database_login["user"],
    database_login["password"],
    database_login["host"],
    database_login["port"],
    database_login["authentication_database"],
)


class MongoDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                print("Connecting to MongoDB...")
                cls._instance = super().__new__(cls)
                cls._instance.client = MongoClient(
                    MONGODB_CONN, maxPoolSize=100, minPoolSize=10
                )
                cls._instance.db = cls._instance.client[
                    database_login["authentication_database"]
                ]
                print("Connected.")
            except Exception as e:
                raise ConnectionError(f"Error connecting to MongoDB: {e}")
        return cls._instance


# Connection to MongoDB
mongo = MongoDB()
db: Database = mongo.db
