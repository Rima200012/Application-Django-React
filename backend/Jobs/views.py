from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import JobPostSerializer, JobApplicationSerializer
from Jobs.connectiondb import get_job_application_collection, get_job_post_collection
from bson import ObjectId
import gridfs
import jwt
from django.conf import settings
from pymongo import MongoClient
from django.http import HttpResponse, Http404
from pdf2image import convert_from_path
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import logging
from rest_framework import status

class JobPostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        published_by = request.query_params.get('published_by')
        query = {}
        if published_by:
            query['published_by'] = ObjectId(published_by)
        posts = list(get_job_post_collection().find(query))
        for post in posts:
            post['_id'] = str(post['_id'])  # Convert ObjectId to string for JSON serialization
            post['published_by'] = str(post['published_by'])  # Convert ObjectId to string
            post['location'] = post.get('location', '')

         # Count number of applicants for each job post
            application_count = get_job_application_collection().count_documents({'job_post_id': ObjectId(post['_id'])})
            post['no_of_applicants'] = application_count
        serializer = JobPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['published_by'] = str(request.user.id)  # Automatically set the published_by field
        serializer = JobPostSerializer(data=data)
        if serializer.is_valid():
            job_post = serializer.save()
            job_post['_id'] = str(job_post['_id'])  # Convert ObjectId to string
            job_post['published_by'] = str(job_post['published_by'])  # Convert ObjectId to string
            job_post['location'] = job_post.get('location', '')
            return Response({"message": "Job post created successfully", "job_post": JobPostSerializer(job_post).data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to add job post", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class JobPostDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return get_job_post_collection().find_one({'_id': ObjectId(id)})
        except:
            return None

    def get(self, request, id):
        job_post = self.get_object(id)
        if job_post is not None:
            serializer = JobPostSerializer(job_post)
            return Response(serializer.data)
        else:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        job_post = self.get_object(id)
        if job_post is not None:
            serializer = JobPostSerializer(job_post, data=request.data)
            if serializer.is_valid():
                updated_job_post = serializer.update(job_post, serializer.validated_data)
                updated_job_post['_id'] = str(updated_job_post['_id'])  # Convert ObjectId to string
                updated_job_post['published_by'] = str(updated_job_post['published_by'])  # Convert ObjectId to string
                return Response({"message": "Job post updated successfully", "job_post": JobPostSerializer(updated_job_post).data})
            return Response({"message": "Failed to update job post", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        job_post = self.get_object(id)
        if job_post is not None:
            get_job_post_collection().delete_one({'_id': ObjectId(id)})
            return Response({"message": "Job post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)


class JobApplicationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        added_by = request.query_params.get('added_by')
        query = {}
        if added_by:
            query['added_by'] = ObjectId(added_by)
        applications = list(get_job_application_collection().find())
        for app in applications:
            app['_id'] = str(app['_id'])  # Convert ObjectId to string for JSON serialization
            app['added_by'] = str(app['added_by'])
            app['job_post_id'] = str(app['job_post_id'])  # Convert ObjectId to string
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['job_post_id'] = request.data.get('job_post_id')
        data['added_by'] = str(request.user.id)  # Automatically set the added_by field

        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            data['resume'] = resume


            # Read the file content once and create a ContentFile object
            resume_content = ContentFile(resume.read())
            resume.seek(0)  # Reset the pointer to the beginning of the file after reading


            # Save the PDF
            path = default_storage.save('resumes/' + resume.name, resume_content)

            

        serializer = JobApplicationSerializer(data=data)
        if serializer.is_valid():
            application = serializer.save()
            application['_id'] = str(application['_id'])  # Convert ObjectId to string
            application['job_post_id'] = str(application['job_post_id'])  # Convert ObjectId to string
            return Response({"message": "Job application created successfully", "application": JobApplicationSerializer(application).data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to add job application", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class JobApplicationDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return get_job_application_collection().find_one({'_id': ObjectId(id)})
        except:
            return None

    def get(self, request, id):
        application = self.get_object(id)
        if application is not None:
            serializer = JobApplicationSerializer(application)
            return Response(serializer.data)
        else:
            return Response({"message": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        application = self.get_object(id)
        if application is not None:
            serializer = JobApplicationSerializer(application, data=request.data)
            if serializer.is_valid():
                updated_application = serializer.update(application, serializer.validated_data)
                updated_application['_id'] = str(updated_application['_id'])  # Convert ObjectId to string
                updated_application['job_post_id'] = str(updated_application['job_post_id'])  # Convert ObjectId to string
                return Response({"message": "Job application updated successfully", "application": JobApplicationSerializer(updated_application).data})
            return Response({"message": "Failed to update job application", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        job_application = self.get_object(id)
        if job_application is not None:
            get_job_application_collection().delete_one({'_id': ObjectId(id)})
            return Response({"message": "Job application deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)



class UpdateApplicationStatus(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id):
        application = get_job_application_collection().find_one({'_id': ObjectId(id)})
        if application is not None:
            status_value = request.data.get('status')
            if status_value:
                get_job_application_collection().update_one(
                    {'_id': ObjectId(id)},
                    {'$set': {'status': status_value}}
                )
                application['status'] = status_value
                return Response(
                    {"message": "Application status updated successfully", "application": JobApplicationSerializer(application).data},
                    status=status.HTTP_200_OK
                )
            return Response({"message": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)
    

logger = logging.getLogger(__name__)

class JobApplicationsByJobPostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_post_id):
        logger.debug(f"Fetching applications for job post ID: {job_post_id}")
        applications = list(get_job_application_collection().find({"job_post_id": job_post_id}))
        for app in applications:
            app['_id'] = str(app['_id'])  # Convert ObjectId to string for JSON serialization
            app['job_post_id'] = str(app['job_post_id'])  # Ensure job_post_id is a string
        if not applications:
            return Response({"message": "No applicants found"}, status=status.HTTP_200_OK)
        serializer = JobApplicationSerializer(applications, many=True)
        logger.debug(f"Applications fetched: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobApplicationCountAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_post_id):
        count = get_job_application_collection().count_documents({"job_post_id": job_post_id})
        return Response({"count": count}, status=status.HTTP_200_OK)
    
class JobPostsByUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Extract user ID from the JWT token
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

            token = auth_header.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')

            if not user_id:
                return Response({"error": "User ID not found in token"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user_id = ObjectId(user_id)  # Convert to ObjectId for MongoDB query
            print(f"Authenticated User ID: {user_id}")  # Debugging statement
        except Exception as e:
            print(f"Error extracting user ID: {e}")  # Debugging statement for error
            return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Query job posts by the authenticated user
            job_posts = list(get_job_post_collection().find({"published_by": user_id}))
            for post in job_posts:
                post['_id'] = str(post['_id'])  # Convert ObjectId to string for JSON serialization
                post['published_by'] = str(post['published_by'])  # Convert ObjectId to string
                post['location'] = post.get('location', '')  # Ensure location is handled correctly
            serializer = JobPostSerializer(job_posts, many=True)
            print(f"Job Posts: {serializer.data}")  # Debugging statement to ensure job posts are retrieved
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error retrieving job posts: {e}")  # Debugging statement for error
            return Response({"error": "Failed to retrieve job posts"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






logger = logging.getLogger(__name__)

class ServeResumeFileView(APIView):
    def get(self, request, file_id):
        db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
        fs = gridfs.GridFS(db)
        try:
            logger.debug(f"Attempting to get file with ID: {file_id}")
            file = fs.get(ObjectId(file_id))
            logger.debug(f"File retrieved: {file.filename}")
            response = HttpResponse(file.read(), content_type=file.content_type)
            response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
            return response
        except gridfs.NoFile:
            logger.error(f"File with ID {file_id} not found")
            raise Http404
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise Http404