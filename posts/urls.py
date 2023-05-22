from django.urls import path

from .views import add_post, get_all_posts, get_category, ShowOnePost, blog_post_like

urlpatterns = [
    path('', get_all_posts, name='home'),
    path('category/<int:category_id>/', get_category, name='category'),
    path('category/<slug:slug>/', ShowOnePost.as_view(), name='one_post'),
    path('add_post/', add_post, name='new'),
    path('category/<slug:slug>/', blog_post_like, name='blogpost_like'),
]
