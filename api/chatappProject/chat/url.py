# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('api/pusher/auth', views.pusher_authentication, name='pusher_authentication'),
]
