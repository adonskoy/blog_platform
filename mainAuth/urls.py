from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.user_register, name='register'),
    path('subscibe/<int:pk>/', views.user_subscribe, name='subscribe')
]
