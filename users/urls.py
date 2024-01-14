from django.urls import path
from users.views.user_login_view import LoginUserAPIView
from users.views.user_profile_view import UserProfileAPIView
from users.views.user_register_view import RegisterUserAPIView

urlpatterns = [
    path('users/register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('users/login/', LoginUserAPIView.as_view(), name='login_user'),
    path('users/<int:userid>/', UserProfileAPIView.as_view(), name='user_profile'),
]
