import pymongo
from api.config import config

class mongodb:
    mongo_db_url = config.mongo_db_url
    database_name = config.database_name

    def insert_one(collection, *args, mongo_db_url=mongo_db_url, database_name=database_name, **kwargs):
        try:
            myclient = pymongo.MongoClient(mongo_db_url)
            try:
                myclient.admin.command('ping')
                print("Connected to MongoDB")
            except Exception as e:
                print(f"Connection failed: {e}")
            collection_name = collection
            database = myclient[database_name]
            collection = database[collection]
            return collection.insert_one(*args, **kwargs)
        except Exception as e:
            print("insert_one", e)