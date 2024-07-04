from django.urls import path
from .views import RecommendCandidatesView

urlpatterns = [
    path('recommend/<str:job_post_id>/', RecommendCandidatesView.as_view(), name='recommend_candidates')
]
