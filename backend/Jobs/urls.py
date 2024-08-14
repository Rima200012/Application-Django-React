from django.urls import path
from django.conf import settings
from .views import JobPostAPIView, JobPostDetailAPIView, JobPostsByUserAPIView, ServeResumeFileView, JobApplicationAPIView, JobApplicationDetailAPIView, JobApplicationsByJobPostAPIView, JobApplicationCountAPIView, UpdateApplicationStatus

urlpatterns = [
    path('jobposts/', JobPostAPIView.as_view(), name='jobpost-list'),
    path('jobposts/<str:id>/', JobPostDetailAPIView.as_view(), name='jobpost-detail'),
    path('jobposts/by-user/', JobPostsByUserAPIView.as_view(), name='jobposts-by-user'),
    path('applications/', JobApplicationAPIView.as_view(), name='job-application-list'),
    path('applications/<str:id>/', JobApplicationDetailAPIView.as_view(), name='job-application-detail'),
    path('applications/<str:id>/status/', UpdateApplicationStatus.as_view(), name='update-application-status'),

    path('jobposts/<str:job_post_id>/applications/', JobApplicationsByJobPostAPIView.as_view(), name='job-applications-by-post'),
    path('jobposts/<str:job_post_id>/applications/count/', JobApplicationCountAPIView.as_view(), name='job_application_count'),

    path('media/<str:file_id>/', ServeResumeFileView.as_view(), name='serve_resume_file'),
]





