from rest_framework import serializers
from Jobs.connectiondb import get_job_application_collection, get_job_post_collection
from bson import ObjectId
import gridfs
from pymongo import MongoClient
from django.conf import settings

class JobPostSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=255, required=False)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    company_name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    published_by = serializers.CharField(max_length=255, required=False)
    is_active = serializers.BooleanField()
    Job_link = serializers.CharField(max_length=255, required=False)

    def create(self, validated_data):
        validated_data['published_by'] = ObjectId(validated_data['published_by'])
        collection = get_job_post_collection()
        job_post_id = collection.insert_one(validated_data).inserted_id
        return collection.find_one({'_id': job_post_id})

    def update(self, instance, validated_data):
        collection = get_job_post_collection()
        collection.update_one({'_id': instance['_id']}, {'$set': validated_data})
        return collection.find_one({'_id': instance['_id']})
    
class JobApplicationSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=255, required=False)
    applicant_name = serializers.CharField(max_length=255)
    job_post_id = serializers.CharField(max_length=24)
    cover_letter = serializers.CharField()
    resume = serializers.FileField()
    added_by = serializers.CharField(max_length=24)

    def create(self, validated_data):
        db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
        fs = gridfs.GridFS(db)

        if 'resume' in validated_data and validated_data['resume']:
            resume = validated_data.pop('resume')
            resume_id = fs.put(resume, filename=resume.name, content_type=resume.content_type)
            validated_data['resume'] = resume_id

        collection = get_job_application_collection()

        result = collection.insert_one(validated_data)
        return collection.find_one({"_id": result.inserted_id})

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['_id'] = str(instance['_id']) if '_id' in instance else None
        ret['resume'] = str(instance['resume']) if 'resume' in instance else None
        return ret