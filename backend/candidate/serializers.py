# candidate/serializers.py
from rest_framework import serializers
from bson import ObjectId
from pymongo import MongoClient
from django.conf import settings
import gridfs
from candidate.connectionsdb import get_candidate_collection

class CandidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    _id = serializers.CharField(max_length=255, required=False)
    state = serializers.CharField(max_length=100)
    added_info = serializers.CharField(max_length=500, required=False, allow_blank=True)
    resume = serializers.FileField()
    added_by = serializers.CharField(max_length=255, required=False)

    def create(self, validated_data):
        db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
        fs = gridfs.GridFS(db)

        if 'resume' in validated_data and validated_data['resume']:
            resume = validated_data.pop('resume')
            resume_id = fs.put(resume, filename=resume.name, content_type=resume.content_type)
            validated_data['resume'] = resume_id

        candidate_collection = get_candidate_collection()
        candidate_id = candidate_collection.insert_one(validated_data).inserted_id
        return candidate_collection.find_one({'_id': candidate_id})

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['_id'] = str(instance['_id']) if '_id' in instance else None
        ret['resume'] = str(instance['resume']) if 'resume' in instance else None
        ret['added_by'] = str(instance['added_by']) if 'added_by' in instance else None
        return ret


    

        