from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:pk>/', views.edit_post, name='edit_post'),
]