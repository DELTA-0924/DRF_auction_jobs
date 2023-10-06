"""
Definition of urls for web_project_veriosn1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home',views.home,name="home"),
    path('/register',views.register,name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('admin/', admin.site.urls),
]
