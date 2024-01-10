from django.urls import path
from users.views import RegisterUserAPIView, LoginUserAPIView, UserProfileAPIView

urlpatterns = [
    path('users/register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('users/login/', LoginUserAPIView.as_view(), name='login_user'),
    path('users/<int:userid>/', UserProfileAPIView.as_view(), name='user_profile'),
]
