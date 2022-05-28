from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'notes'

router = routers.DefaultRouter()
router.register('notes', views.NoteViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
