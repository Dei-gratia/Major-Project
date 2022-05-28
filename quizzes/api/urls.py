from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'quizzes'

router = routers.DefaultRouter()
router.register('quizzes', views.QuizViewSet)
router1 = routers.DefaultRouter()
router1.register('questions', views.QuestionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('quizzes/<quiz_id>/', include(router1.urls)),
]
