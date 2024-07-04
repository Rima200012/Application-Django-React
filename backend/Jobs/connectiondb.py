from pymongo import MongoClient
from django.conf import settings

def get_job_post_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db['job_posts']

def get_job_application_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db['job_applications']

