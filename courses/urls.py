from django.urls import path

from main.views import search
from . import views
urlpatterns = [
    path('',	views.CourseListView.as_view(),	name='course_list'),


    path('mine/',
         views.ManageCourseListView.as_view(),
         name='manage_course_list'),

    path('create/',
         views.CourseCreateView.as_view(),
         name='course_create'),

    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course_edit'),

    path('<pk>/delete/',
         views.CourseDeleteView.as_view(),
         name='course_delete'),

    path('<pk>/module/',
         views.CourseModuleUpdateView.as_view(),
         name='course_module_update'),

    path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),

    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),

    path('content/<int:id>/delete/',
         views.ContentDeleteView.as_view(),
         name='module_content_delete'),

    path('module/<int:module_id>/',
         views.ModuleContentListView.as_view(),
         name='module_content_list'),

    path('module/order/',
         views.ModuleOrderView.as_view(),
         name='module_order'),

    path('content/order/',
         views.ContentOrderView.as_view(),
         name='content_order'),

    path('subject/<slug:subject>)/<order>/',
         views.CourseListView.as_view(),
         name='course_list_subject'),

    path('school_level/<slug:school_level>/<order>/',
         views.CourseListView.as_view(),
         name='course_list_level'),

    path('school_level/<slug:school_level>/subject/<slug:subject>)/<order>/',
         views.CourseListView.as_view(),
         name='course_list_level_subject'),



    path('course/<slug:slug>/',
         views.CourseDetailView.as_view(),
         name='course_detail'),

    path('<order>/',	views.CourseListView.as_view(),	name='course_list'),

    path('all/search/', views.search, name='course_search'),

]
