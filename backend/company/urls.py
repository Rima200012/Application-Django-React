from django.urls import path
from .views import CompanyAPIView, CompanyDetailAPIView

urlpatterns = [
    path('companies/', CompanyAPIView.as_view(), name='company-list'),
    path('companies/<str:id>/', CompanyDetailAPIView.as_view(), name='company-detail'),
]
