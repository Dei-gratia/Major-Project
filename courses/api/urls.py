from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'courses'

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router1 = routers.DefaultRouter()
router1.register('modules', views.ModuleViewSet)
router2 = routers.DefaultRouter()
router2.register('contents', views.ModuleContentsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('courses/<course_id>/', include(router1.urls)),
    path('courses/<course_id>/modules/<module_id>/', include(router2.urls)),
]
