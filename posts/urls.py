from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:pk>/', views.edit_post, name='edit_post'),
    path('delete-post/<str:pk>/', views.delete_post, name='delete_post'),
    path('post/<str:pk>/', views.post, name='post'),
    path('comment-post/<str:pk>/', views.comment_post, name='comment_post'),
    path('vote-post/<str:pk>/', views.vote_post, name='vote_post'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete_comment'),
    
    path('posts-json/<int:num_posts>/', views.posts_json, name='posts_json'),

    path('comments-json/<str:post_id>/', views.comments_json, name='comments_json'),
]