from django.urls import path
from .views import CandidateAPIView, CandidateDetailAPIView, ServeResumeFileView

urlpatterns = [
    path('candidates/', CandidateAPIView.as_view(), name='candidates-list'),
    path('candidate/<str:id>/', CandidateDetailAPIView.as_view(), name='candidate-detail'),
    path('media/<str:file_id>/', ServeResumeFileView.as_view(), name='serve_resume_file'),
]