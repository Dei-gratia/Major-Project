from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'main'

router = routers.DefaultRouter()
router.register('school_levels', views.SchoolLevelViewSet)
router.register('specilisations', views.SpecialisationViewSet)
router.register('programs', views.ProgramViewSet)
router.register('subjects', views.SubjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
