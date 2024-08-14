from django.urls import path
from .views import ActiveJobPostsView, get_embed_config, UserApplicationsView, TotalApplicationsView, JobApplicationStatusView, ConversionRateView, AverageTimeToFillView, ApplicationsPerPostView, AcceptanceRateView, generate_embed_token
    

urlpatterns = [
    path('active-job-posts/', ActiveJobPostsView.as_view(), name='active_job_posts'),
    path('total-applications/', TotalApplicationsView.as_view(), name='total_applications'),
    path('conversion-rate/', ConversionRateView.as_view(), name='conversion_rate'),
    path('applications-per-post/', ApplicationsPerPostView.as_view(), name='applications_per_post'),
    path('average-fill-time/', AverageTimeToFillView.as_view(), name='average_fill_time'),
    path('job-application-status/', JobApplicationStatusView.as_view(), name='job_application_status'),
    path('user-applications/<str:user_id>/', UserApplicationsView.as_view(), name='user_applications'),
    path('acceptance-rate/', AcceptanceRateView.as_view(), name='acceptance_rate'),
    path('api/get_embed_config/<str:user_type>/', get_embed_config),
    path('api/get_embed_token/', generate_embed_token),
    

]
