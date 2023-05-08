from django.urls import include, re_path, path

from .views import ChangeProfile, LoginUser, \
    MyPasswordResetConfirmView, MySignupView, Register, activate_account, user_profile

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', LoginUser.as_view(template_name='registration/login.html'), name='login'),
    path('actative/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate_account, name='activate'),
    path('social/signup/', MySignupView.as_view(template_name='registration/signup_google.html'),
         name='account_signup'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', include('django.contrib.auth.urls')),
    path('change_profile/<int:pk>/', ChangeProfile.as_view(), name='change_profile'),
    path('user_profile/<int:pk>/', user_profile, name='user_profile'),
    path('', include("allauth.urls")),
]
