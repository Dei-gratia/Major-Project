from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_view, name='login'),

    path('logout', views.logout_view, name='logout'),

    path('password_reset', views.password_reset, name='password_reset'),

    path('email_reset', views.email_reset, name='email_reset'),

    path('<pk>/user_profile', views.UserProfile.as_view(), name='user_profile'),
    #path('dashboard', views.dashboard, name='dashboard'),

    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),

    path('courses/',
         views.StudentCourseListView.as_view(),
         name='student_course_list'),

    path('course/<pk>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail'),

    path('course/<pk>/<module_id>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),

]
