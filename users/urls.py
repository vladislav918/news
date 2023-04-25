from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', LoginUser.as_view(template_name='registration/login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('change_profile/<int:pk>/', ChangeProfile.as_view(), name='change_profile'),
]
