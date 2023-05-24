from django.urls import path

from .views import AddPost, AllPosts, CategoryView, ShowOnePost, blog_post_like, ChangePosts

urlpatterns = [
    path('', AllPosts.as_view(), name='home'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),
    path('category/<slug:slug>/', ShowOnePost.as_view(), name='one_post'),
    path('add_post/', AddPost.as_view(), name='new'),
    path('category/<slug:slug>/', blog_post_like, name='blogpost_like'),
    path('changeposts/<slug:slug>/', ChangePosts.as_view(), name='change_posts'),
]
