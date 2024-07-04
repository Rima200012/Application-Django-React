from company.connectiondb import get_company_collection
from rest_framework import serializers

class CompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    contact = serializers.CharField(max_length=255)
    
    state = serializers.CharField(max_length=100)
    field_of_work = serializers.CharField(max_length=255)
    added_info = serializers.CharField(max_length=500, required=False, allow_blank=True)

    

    def create(self, validated_data):

       
        company_collection = get_company_collection()
        company_id = company_collection.insert_one(validated_data).inserted_id
        return company_collection.find_one({'_id': company_id})

    def update(self, instance, validated_data):
        company_collection = get_company_collection()
        company_collection.update_one({'_id': instance['_id']}, {'$set': validated_data})
        return company_collection.find_one({'_id': instance['_id']})
