from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from company.connectiondb import get_company_collection
from company.serializers import CompanySerializer
from bson import ObjectId
from users.permissions import allowed_roles



class CompanyAPIView(APIView):
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        companies = list(get_company_collection().find())
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)
    
    
    @allowed_roles(['recruiter'])
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save()
            return Response({"message": "Company profile created successfully", "company": CompanySerializer(company).data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to add company", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetailAPIView(APIView):
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, id):
        try:
            return get_company_collection().find_one({'_id': ObjectId(id)})
        except:
            return None

    def get(self, request, id):
        company = self.get_object(id)
        if company is not None:
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        else:
            return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @allowed_roles(['recruiter'])
    def put(self, request, id):
        company = self.get_object(id)
        if company is not None:
            serializer = CompanySerializer(company, data=request.data)
            if serializer.is_valid():
                updated_company = serializer.update(company, serializer.validated_data)
                return Response({"message": "Company updated successfully", "company": CompanySerializer(updated_company).data})
            return Response({"message": "Failed to update company", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @allowed_roles(['recruiter'])
    def delete(self, request, id):
        company = self.get_object(id)
        if company is not None:
            get_company_collection().delete_one({'_id': ObjectId(id)})
            return Response({"message": "Company deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)


   
