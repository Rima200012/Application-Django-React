from pymongo import MongoClient
from django.conf import settings
import gridfs

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

fs = gridfs.GridFS(db)

class JobPost:
    collection = db['job_posts']

    @staticmethod
    def find_one(job_post_id):
        return JobPost.collection.find_one({"_id": job_post_id})

    
class Resume:
    collection = db['fs.files']

    @staticmethod
    def find_all():
        return Resume.collection.find()




