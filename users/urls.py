from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('actative/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate_account, name='activate'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/', LoginUser.as_view(template_name='registration/login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('change_profile/<int:pk>/', ChangeProfile.as_view(), name='change_profile'),
]
