from Jobs.connectiondb import get_job_post_collection
from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import recommend_candidates

class RecommendCandidatesView(APIView):
    def get(self, request, job_post_id):
        try:
            job_posts = get_job_post_collection()
            job_post = job_posts.find_one({"_id": ObjectId(job_post_id)})
            if not job_post:
                return Response({"error": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)

            job_description = job_post.get('description', '')
            if not job_description:
                return Response({"error": "Job description is missing"}, status=status.HTTP_404_NOT_FOUND)

            print("Job Description:", job_description)  # Debugging statement

            recommendations = recommend_candidates(job_description)

            print("Recommendations:", recommendations)  # Debugging statement

            return Response({"recommendations": recommendations}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error in RecommendCandidatesView:", e)  # Debugging statement
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)