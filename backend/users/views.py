from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from rest_framework import status, permissions
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, CustomTokenRefreshSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from users.authentications import get_user_collection
from bson import ObjectId
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import bcrypt
import pymongo
from django.shortcuts import redirect

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.utils.http import urlsafe_base64_decode
import jwt
from datetime import datetime, timedelta
from pymongo import MongoClient
from .authentications import MongoUser
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["demodatabase"]
users_collection = db["users"]

class CustomTokenObtainPairView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data.get('email')
            
            user = db.users.find_one({'email': user_email})

            if user and not user.get('email_verified', False):
                return Response({"detail": "You need to verify your account via your email."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


def send_welcome_email(to_email):
    subject = 'Welcome to Our Site'
    message = 'Hello, thank you for registering at our site.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        print("Email sent successfully to", to_email)
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False


def generate_verification_token(user):
    payload = {
        'user_id': str(user['_id']),  # Convert ObjectId to string
        'email': user['email'],
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expiration time
        'iat': datetime.utcnow(),  # Issued at time
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def send_verification_email(user_dict):
    user = MongoUser(user_dict)
    token = str(AccessToken.for_user(user))
    uid = urlsafe_base64_encode(force_bytes(user._id))
    verification_link = f"http://localhost:5173/verify_email/{uid}/{token}/"

    send_mail(
        'Verify your email',
        f'Click the link to verify your email: {verification_link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


class UserCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            user = serializer.save()

            # Send verification email
            send_verification_email(user)

            return Response({
                "user": UserSerializer(user).data,
                "message": "User created successfully. Please check your email to verify your account."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id):
        # Update an existing user
        user = self.get_object(id)
        if user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                updated_user = serializer.save()
                return Response({
                    "user": UserSerializer(updated_user).data,
                    "message": "User updated successfully"
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        # Delete a user
        user = self.get_object(id)
        if user:
            get_user_collection().delete_one({'_id': ObjectId(id)})
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user_id = request.user.id
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    if not user:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not bcrypt.checkpw(old_password.encode(), user['password']):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        hashed_new_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'password': hashed_new_password}}
        )
        return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):
    user = users_collection.find_one({'_id': ObjectId(request.user.id)})
    if user:
        return Response({'role': user.get('role')})
    return Response({'error': 'User not found'}, status=404)

@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
 
    user = users_collection.find_one({'_id': ObjectId(request.user.id)})
    if user:
        user['_id'] = str(user['_id'])
        return Response({
            "user": {
                "id": user['_id'],
                "username": user['username'],
                "email": user['email'],
                "role": user.get('role')
            }
        }, status=status.HTTP_200_OK)
    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user_id = ObjectId(uid)

            try:
                AccessToken(token)  # Verify token
            except TokenError:
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            # Connect to MongoDB and update the user's email verification status
            client = MongoClient(settings.MONGO_URI)
            db = client[settings.MONGO_DB_NAME]
            users_collection = db['users']
            user = users_collection.find_one({"_id": user_id})

            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Mark the email as verified
            users_collection.update_one({"_id": user_id}, {"$set": {"email_verified": True}})
            
            # Redirect to frontend login page with a message
            return redirect(f"http://localhost:5173/login?verified=true")

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.permissions import BasePermission

class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.email_verified
