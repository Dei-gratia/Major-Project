from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'discussions'

router = routers.DefaultRouter()
router.register('discussion_topics', views.DiscussionTopicViewSet)
router1 = routers.DefaultRouter()
router1.register('posts', views.PostViewSet)
router2 = routers.DefaultRouter()
router2.register('replies', views.ReplieViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('discussion_topics/<topic_id>/', include(router1.urls)),
    path('discussion_topics/<topic_id>/posts/<post_id>/', include(router2.urls)),
]
