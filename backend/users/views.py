from rest_framework.views import APIView
from rest_framework.response import Response
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

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["demodatabase"]
users_collection = db["users"]

class CustomTokenObtainPairView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class UserCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            
            return Response({
                "user": UserSerializer(user).data,
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            # Check if the error is due to the user existing or other validation failures
            if 'email' in serializer.errors and 'already exists' in serializer.errors['email'][0]:
                message = "User already exists"
            else:
                message = "Failed to create user"
            
            return Response({
                "errors": serializer.errors,
                "message": message
            }, status=status.HTTP_400_BAD_REQUEST)
    
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