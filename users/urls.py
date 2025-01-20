from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('check-username/', views.check_username, name='check_username'),

    path('profile/<username>/', views.profile, name='user_profile'),
    path('my-profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('add-social/', views.add_social, name='add_social'),
    path('edit-social/<str:pk>/', views.edit_social, name='edit_social'),
    path('delete-social/<str:pk>/', views.delete_social, name='delete_social'),
]