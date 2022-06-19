from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='admin_dashboard'),

    path('users/', views.UsersView.as_view(), name='back_user_list'),
    path('users/<pk>/delete', views.UserDeleteView.as_view(),
         name='back_user_delete'),
    path('users/<pk>/edit', views.UserUpdateView.as_view(),
         name='back_user_edit'),
    path('users/create', views.UserCreateView.as_view(), name='back_user_create'),

    path('contacts/', views.ContactsView.as_view(), name='back_contact_list'),
    path('contacts/<pk>/delete', views.ContactDeleteView.as_view(),
         name='back_contact_delete'),

    path('courses/', views.CoursesView.as_view(), name='back_course_list'),
    path('courses/<pk>/delete', views.CourseDeleteView.as_view(),
         name='back_course_delete'),
    path('courses/<pk>/edit', views.CourseUpdateView.as_view(),
         name='back_course_edit'),

    path('notes/', views.NotesView.as_view(), name='back_note_list'),
    path('notes/<pk>/delete', views.NoteDeleteView.as_view(),
         name='back_note_delete'),
    path('notes/<pk>/edit', views.NoteUpdateView.as_view(),
         name='back_note_edit'),

    path('quizzes/', views.QuizzesView.as_view(), name='back_quiz_list'),
    path('quizzes/<pk>/delete', views.QuizDeleteView.as_view(),
         name='back_quiz_delete'),
    path('quizzes/<pk>/edit', views.QuizUpdateView.as_view(),
         name='back_quiz_edit'),

    path('discussion_topics/', views.DiscussionTopicView.as_view(),
         name='back_topic_list'),
    path('discussion_topics/<pk>/delete', views.DiscussionTopicDeleteView.as_view(),
         name='back_topic_delete'),
    path('discussion_topics/<pk>/edit', views.DiscussionTopicUpdateView.as_view(),
         name='back_topic_edit'),

    path('posts/', views.PostsView.as_view(), name='back_post_list'),
    path('posts/create', views.PostCreateView.as_view(), name='back_post_create'),
    path('posts/<pk>/delete', views.PostDeleteView.as_view(),
         name='back_post_delete'),
    path('posts/<pk>/edit', views.PostUpdateView.as_view(),
         name='back_post_edit'),

    path('replies/', views.ReplieView.as_view(), name='back_replie_list'),
    path('replies/create', views.ReplieCreateView.as_view(),
         name='back_replie_create'),
    path('replies/<pk>/delete', views.ReplieDeleteView.as_view(),
         name='back_replie_delete'),
    path('replies/<pk>/edit', views.ReplieUpdateView.as_view(),
         name='back_replie_edit'),
]
