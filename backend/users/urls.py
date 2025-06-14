

from django.urls import path
from .views import UserCreateAPIView, get_user_role, get_user_profile, change_password, VerifyEmailView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('get_user_role/', get_user_role, name='user-role'),
    path('users/me/', get_user_profile, name='user-profile'),  # New endpoint for user profile
    path('password/', change_password, name='change-password'),
    path('verify_email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),

]
