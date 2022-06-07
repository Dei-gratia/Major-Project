from rest_framework import routers
from django.urls import path, include
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('',
         views.UserListView.as_view(),
         name='user_list'),

    path('<pk>/',
         views.UserDetailView.as_view(),
         name='user_detail'),

    path('<pk>/profile/',
         views.ProfileDetailView.as_view(),
         name='profile_detail'),
]
