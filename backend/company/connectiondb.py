from pymongo import MongoClient
from django.conf import settings

def get_company_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db['company']

