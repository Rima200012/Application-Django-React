from rest_framework import serializers
from users.authentications import get_user_collection
from pymongo import MongoClient
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings




class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.CharField(max_length=100)  # Not write_only to allow for role checks
    phone = serializers.CharField(max_length=20, required=False)
    address = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)
    country = serializers.CharField(max_length=100, required=False)

    def validate_email(self, value):
        # MongoDB query to check if email already exists
        db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
        if db.users.find_one({"email": value}):
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        user_collection = get_user_collection()
        # Hash the password before saving
        validated_data['password'] = bcrypt.hashpw(validated_data['password'].encode(), bcrypt.gensalt())

        # Save the user with role in MongoDB
        user_id = user_collection.insert_one(validated_data).inserted_id
        return user_collection.find_one({'_id': user_id})

    def to_representation(self, instance):
        """Convert MongoDB documents, which include ObjectId, to a more JSON-friendly format."""
        representation = super().to_representation(instance)
        representation['_id'] = str(instance['_id'])
        # Optionally add role to the representation if needed
        representation['role'] = instance.get('role', 'default_role')
        return representation
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Use email as the identifier
    @classmethod
    def get_token(cls, user):
        token = RefreshToken()
        token['user_id'] = str(user['_id'])  # Convert ObjectId to string
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
        user = db.users.find_one({'email': email})

        if user and bcrypt.checkpw(password.encode(), user['password']):
            refresh = self.get_token(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user['email'],
                'role': user['role']
            }
        else:
            raise serializers.ValidationError('No active account found with the given credentials')
        
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom data or perform additional checks
        data['custom_data'] = 'value'
        return data