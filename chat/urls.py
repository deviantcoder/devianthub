from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('start-chat/<username>/', views.get_or_create_chat, name='get_or_create_chat'),
    path('chatroom/<chatroom_name>/', views.chat, name='chatroom'),
    path('create-group/', views.create_group, name='create_group'),
    path('edit-group/<chat_name>/', views.edit_group, name='edit_group'),
    path('delete-group/<chat_name>/', views.delete_group, name='delete_group'),
    path('leave-group/<chat_name>/', views.leave_group, name='leave_group'),
]