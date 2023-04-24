from django.urls import path, include
from django.views.generic import TemplateView
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', get_all_posts, name='home'),
    path('category/<int:category_id>/', get_category, name='category'),
    path('category/<slug:slug>/', Show_one_post.as_view(), name='one_post'),
    path('add_post/', add_post, name='new'),
]
