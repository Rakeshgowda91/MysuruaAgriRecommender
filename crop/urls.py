# crop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    
    # New URLs for authentication and profile
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]