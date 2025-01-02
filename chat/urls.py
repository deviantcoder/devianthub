from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('start/<username>/', views.get_or_create_chat, name='get_or_create_chat'),
    path('chatroom/<chatroom_name>/', views.chat, name='chatroom'),
    path('test/', views.test)
]