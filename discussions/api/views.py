from pydoc_data.topics import topics
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import TopicSerializer, TopicDetailSerializer, PostSerializer, \
    PostDetailSerializer, PostCreateSerializer, TopicCreateSerializer, ReplieCreateSerializer, ReplieSerializer
from ..models import DiscussionTopic, Post, Replie
from courses.models import Subject
from main.mixins import GetSerializerClassMixin
from django.http import Http404


class DiscussionTopicViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = DiscussionTopic.objects.all()
    serializer_class = TopicDetailSerializer
    serializer_action_classes = {
        'list': TopicSerializer,
        'create': TopicCreateSerializer,
        'update': TopicCreateSerializer
    }

    filterset_fields = ("school_level", "subject", "number_of_posts", )
    search_fields = ("title", )
    ordering_fields = ("title", "total_posts", )
    ordering = ("-date", )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            DiscussionTopic.objects.create(
                owner=self.request.user,  **validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.subject = validated_data.get("subject", instance.subject)
            instance.title = validated_data.get("title", instance.title)
            instance.school_level = validated_data.get(
                "school_level", instance.school_level)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {
                'message': 'discussion topic with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'discussion topic deleted successfully'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


class PostViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        'list': PostSerializer,
        'create': PostCreateSerializer,
        'update': PostCreateSerializer,
    }

    filterset_fields = ("discussion_topic", "owner", )
    search_fields = ("title", 'post_content')
    ordering_fields = ("title", "date", "total_replies")
    ordering = ("-date", )

    def get_queryset(self):
        discussion_topic = DiscussionTopic.objects.get(
            id=self.kwargs['topic_id'])
        return Post.objects.filter(discussion_topic=discussion_topic)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            discussion_topic = DiscussionTopic.objects.get(
                id=self.kwargs['topic_id'])
            Post.objects.create(owner=request.user,
                                discussion_topic=discussion_topic, **validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.post_content = validated_data.get(
                "post_content", instance.post_content)
            instance.image = validated_data.get("image", instance.image)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'post with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'post deleted successfully'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


class ReplieViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = ReplieSerializer
    serializer_action_classes = {
        'list': ReplieSerializer,
        'create': ReplieCreateSerializer,
        'update': ReplieCreateSerializer,
    }

    filterset_fields = ("post", "user", 'date')
    search_fields = ("replie_content", )
    ordering_fields = ("date", )
    ordering = ("-date", )

    def get_queryset(self):
        post = Post.objects.get(id=self.kwargs['post_id'])
        return Replie.objects.filter(post=post)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            post = Post.objects.get(
                id=self.kwargs['post_id'])
            Replie.objects.create(user=request.user,
                                  post=post, **validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.replie_content = validated_data.get(
                "replie_content", instance.replie_content)
            instance.image = validated_data.get("image", instance.image)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'reply with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'reply deleted successfully'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
