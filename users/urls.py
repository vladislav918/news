from django.conf import settings
from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path('register/', usersignup, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('email/', email_confirm, name='email_confirm'),
    path('change_profile/<int:pk>/', Change_profile.as_view(), name='change_profile'),
]
