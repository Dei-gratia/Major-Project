from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .permissions import IsEnrolled
from .serializers import ContentSerializer, CourseWithContentsSerializer
from .serializers import CourseSerializer, CourseDetailSerializer, CourseCreateSerializer, ModuleSerializer, ModuleWithContentsSerializer
from ..models import Course, Subject, Module, SchoolLevel, Content
from django.http import Http404
from main.mixins import GetSerializerClassMixin


class CourseViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    serializer_action_classes = {
        'list': CourseSerializer,
        'create': CourseCreateSerializer,
        'update': CourseCreateSerializer,
    }

    filterset_fields = ('school_level', "subject", "average_rating", "owner")
    search_fields = ("title", "overview", )
    ordering_fields = ("title", )
    ordering = ("-created", )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            Course.objects.create(
                owner=self.request.user, slug=validated_data.get('title'), **validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.school_level = validated_data.get("school_level")
            instance.subject = validated_data.get("subject")
            instance.title = validated_data.get("title", instance.title)
            instance.overview = validated_data.get(
                "overview", instance.overview)
            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'course with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'course deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    @ action(detail=True, methods=['post'],
             authentication_classes=[BasicAuthentication],
             permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @ action(detail=True, methods=['get'],
             serializer_class=CourseWithContentsSerializer,
             authentication_classes=[BasicAuthentication],
             permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ModuleViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        print(self.kwargs)
        course = Course.objects.get(id=self.kwargs['course_id'])
        return Module.objects.filter(course=course)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            course = Course.objects.get(id=self.kwargs['course_id'])
            print(course)
            Module.objects.create(course=course, **validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.title = validated_data.get("title", instance.title)
            instance.order = validated_data.get("order", instance.order)
            instance.description = validated_data.get(
                "description", instance.description)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'module with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'module deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


class ModuleContentsViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_queryset(self):
        print(self.kwargs)
        module = Module.objects.get(id=self.kwargs['module_id'])
        return Content.objects.filter(module=module)

    @ action(detail=True, methods=['get'],
             serializer_class=ContentSerializer,
             # authentication_classes=[BasicAuthentication],
             # permission_classes=[IsAuthenticated, IsEnrolled]
             )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            module = Module.objects.get(id=self.kwargs['module_id'])
            print(module)
            Content.objects.create(module=module, **validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.title = validated_data.get("title", instance.title)
            instance.order = validated_data.get("order", instance.order)
            instance.description = validated_data.get(
                "description", instance.description)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'module with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'module deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
