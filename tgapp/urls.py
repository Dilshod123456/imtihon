from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='views'),
    path('bot/', views.bot_view, name='bot_view'),
]
