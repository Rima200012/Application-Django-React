from rest_framework import authentication, exceptions
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings
import bcrypt

def get_user_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db['users']

# Fonction pour créer un compte superuser
def create_superuser():
    user_collection = get_user_collection()
    if not user_collection.find_one({"role": "superuser"}):
        superuser = {
            "username": "admin",
            "email": "admin@example.com",
            "password": bcrypt.hashpw("admin_password".encode(), bcrypt.gensalt()),
            "role": "superuser"
        }
        user_collection.insert_one(superuser)
        
class MongoUser:
    def __init__(self, user_dict):
        self._user_dict = user_dict

    def __getattr__(self, email):
        # Default getattr to support Django's user model attributes like is_authenticated, etc.
        return self._user_dict.get(email)

    @property
    def is_authenticated(self):
        # Always return True to comply with Django's authentication system checks
        return True

    @property
    def id(self):
        # Return user's '_id' from MongoDB
        return self._user_dict.get('_id')
    
    @property
    def _id(self):
        # Alias for the 'id' attribute
        return str(self._user_dict.get('_id'))
    
    @property
    def email(self):
        # Get email from user dictionary
        return self._user_dict.get('email')


class MongoDBJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        raw_token = authentication.get_authorization_header(request).split()
        if not raw_token or raw_token[0].lower() != b'bearer':
            return None

        try:
            token = raw_token[1]
            validated_token = UntypedToken(token)
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except (InvalidToken, TokenError) as e:
            raise exceptions.AuthenticationFailed('Invalid token') from e

        user_collection = get_user_collection()
        user_dict = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user_dict:
            raise exceptions.AuthenticationFailed('User not found')

        # Wrap the dictionary in our MongoUser class
        user = MongoUser(user_dict)
        return (user, token)
