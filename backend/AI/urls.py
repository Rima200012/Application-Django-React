from django.urls import path
from .views import ResumeSimilarityView, EvaluateKMeansView, LastSavedRecommendationsView

urlpatterns = [
    path('resume_similarity/<str:job_post_id>/', ResumeSimilarityView.as_view(), name='resume_similarity'),
    path('last-recommendations/<str:job_post_id>/', LastSavedRecommendationsView.as_view(), name='last_recommendations'),

    path('evaluate-kmeans/', EvaluateKMeansView.as_view(), name='evaluate_kmeans'),
]

