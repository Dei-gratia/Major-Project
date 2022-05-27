from django.urls import path
from . import views

urlpatterns = [
    path('user_profile', views.user_profile, name='user_profile'),
    #path('dashboard', views.dashboard, name='dashboard'),
]
