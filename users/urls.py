from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_user, name='logout'),
    path('check-username/', views.check_username, name='check_username'),
]