from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # import this

urlpatterns = [

    path('login/', views.login_view, name='login'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('logout', views.logout_view, name='logout'),

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

    path('<pk>/dashboard/', views.DashboardView.as_view(), name='dashboard'),

    path('password_reset', views.password_reset, name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='front/users/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="front/users/password_reset_confirm.html"), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='front/users/password_reset_complete.html'), name='password_reset_complete'),

]
