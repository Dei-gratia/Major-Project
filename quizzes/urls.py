from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),

    path('<quiz_id>/questions/',
         views.QuizQuestionListView.as_view(), name='start_quiz'),

    path('<int:pk>/',
         views.QuizDetailView.as_view(),
         name='quiz_detail'),
    path('mine/',
         views.ManageQuizListView.as_view(),
         name='manage_quiz_list'),

    path('create/',
         views.QuizCreateView.as_view(),
         name='quiz_create'),

    path('<pk>/edit/',
         views.QuizUpdateView.as_view(),
         name='quiz_edit'),

    path('<pk>/delete/',
         views.QuizDeleteView.as_view(),
         name='quiz_delete'),

    path('<pk>/edit/questions/',
         views.QuizQuestionUpdateView.as_view(),
         name='quiz_questions_update'),

    path('questions/order/',
         views.QuestionOrderView.as_view(),
         name='questions_order'),

    path('subject/<slug:subject>)/<order>/',
         views.QuizListView.as_view(),
         name='quiz_list_subject'),

    path('school_level/<slug:school_level>/<order>/',
         views.QuizListView.as_view(),
         name='quiz_list_level'),

    path('school_level/<slug:school_level>/subject/<slug:subject>)/<order>/',
         views.QuizListView.as_view(),
         name='quiz_list_level_subject'),

    path('quiz/<slug:slug>/',
         views.QuizDetailView.as_view(),
         name='quiz_detail'),

    path('<order>', views.QuizListView.as_view(), name='quiz_list'),

]
