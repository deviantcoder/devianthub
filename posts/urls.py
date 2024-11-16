from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:pk>/', views.edit_post, name='edit_post'),
    path('delete-post/<str:pk>/', views.delete_post, name='delete_post'),
    path('post/<str:pk>/', views.post, name='post'),
    path('vote-post/<str:pk>/', views.vote_post, name='vote_post'),
]