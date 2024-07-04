from pymongo import MongoClient
from django.conf import settings

def get_candidate_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db['candidate']

    

