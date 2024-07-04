from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from candidate.connectionsdb import get_candidate_collection
from candidate.serializers import CandidateSerializer
from bson import ObjectId
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import gridfs
from django.conf import settings
from pymongo import MongoClient
from django.http import HttpResponse, Http404
import logging

class CandidateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        added_by = request.query_params.get('added_by')
        query = {}
        if added_by:
            query['added_by'] = added_by
        candidates = list(get_candidate_collection().find(query))
        for candidate in candidates:
            candidate['_id'] = str(candidate['_id'])
            candidate['added_by'] = str(candidate['added_by'])

        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['added_by'] = str(request.user.id)  # Automatically set the added_by field

        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            data['resume'] = resume


            # Read the file content once and create a ContentFile object
            resume_content = ContentFile(resume.read())
            resume.seek(0)  # Reset the pointer to the beginning of the file after reading


            # Save the PDF
            path = default_storage.save('resumes/' + resume.name, resume_content)

        serializer = CandidateSerializer(data=data)
        if serializer.is_valid():
            candidate = serializer.save()
            candidate['_id'] = str(candidate['_id'])  # Convert ObjectId to string
            return Response({"message": "Candidate profile created successfully", "candidate": CandidateSerializer(candidate).data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to add candidate", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class CandidateDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return get_candidate_collection().find_one({'_id': ObjectId(id)})
        except:
            return None

    def get(self, request, id):
        candidate = self.get_object(id)
        if candidate is not None:
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)
        else:
            return Response({"message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        candidate = self.get_object(id)
        if candidate is not None:
            serializer = CandidateSerializer(candidate, data=request.data)
            if serializer.is_valid():
                updated_candidate = serializer.update(candidate, serializer.validated_data)
                updated_candidate['_id'] = str(updated_candidate['_id'])  # Convert ObjectId to string
                return Response({"message": "Candidate updated successfully", "candidate": CandidateSerializer(updated_candidate).data})
            return Response({"message": "Failed to update candidate", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        candidate = self.get_object(id)
        if candidate is not None:
            get_candidate_collection().delete_one({'_id': ObjectId(id)})
            return Response({"message": "Candidate deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)



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