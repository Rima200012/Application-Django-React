from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TestModel  # Ensure this is a very basic model

class TestAPIView(APIView):
    def get(self, request):
        data = TestModel.objects.all()  # Should be a simple model
        return Response({"data": list(data.values())})
