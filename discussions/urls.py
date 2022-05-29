from django.urls import path
from . import views

urlpatterns = [
    path('', views.DiscussionTopicListView.as_view(),
         name='discussion_topic_list'),

    path('<topic_id>/posts/',
         views.DiscussionPostListView.as_view(), name='post_list'),

    path('<topic_id>/posts/<post_id>/',
         views.DiscussionPostDetailView.as_view(), name='post_detail'),

    path('<int:pk>/',
         views.DiscussionTopicDetailView.as_view(),
         name='discussion_topic_detail'),
    path('mine/',
         views.ManageDiscussionListView.as_view(),
         name='manage_discussion_topic_list'),

    path('create/',
         views.DiscussionCreateView.as_view(),
         name='discussion_topic_create'),

    path('<pk>/edit/',
         views.DiscussionUpdateView.as_view(),
         name='discussion_topic_edit'),

    path('<pk>/delete/',
         views.DiscussionDeleteView.as_view(),
         name='discussion_topic_delete'),

    path('<pk>/posts/',
         views.DiscussionPostUpdateView.as_view(),
         name='discussion_topic_post_update'),

    path('subject/<slug:subject>)/',
         views.DiscussionTopicListView.as_view(),
         name='discussion_topic_list_subject'),

]
