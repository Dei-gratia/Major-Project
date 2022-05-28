from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from main.mixins import GetSerializerClassMixin
from .serializers import NoteSerializer, NoteDetailSerializer, NoteCreateSerializer
from ..models import Note
from main.models import Subject


class NoteViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteDetailSerializer
    serializer_action_classes = {
        'list': NoteSerializer,
        'create': NoteCreateSerializer,
        'update': NoteCreateSerializer,
    }
    # authentication_classes=[BasicAuthentication]
    # permission_classes=[IsAuthenticated]

    filterset_fields = ("level", "subject", "average_rating", )
    search_fields = ("title", "description", "body", )
    ordering_fields = ("title", "average_rating", )
    ordering = ("-created_date", )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            Note.objects.create(
                owner=self.request.user, **validated_data)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.school_level = validated_data.get(
                "school_level", instance.school_level)
            instance.subject = Subject.objects.get(
                title=validated_data.get("subject"))
            instance.title = validated_data.get("title", instance.title)
            instance.description = validated_data.get(
                "description", instance.description)
            instance.body = validated_data.get("body", instance.body)
            instance.tags = validated_data.get("tags", instance.tags)
            instance.cover_img = validated_data.get(
                "cover_img", instance.cover_img)
            instance.file = validated_data.get("file", instance.file)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'note with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'note successfully deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
