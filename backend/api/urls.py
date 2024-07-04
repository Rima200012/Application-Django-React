#we're going to forward URLs from the main application to here
from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.TestAPIView.as_view(), name = "APItest")
]