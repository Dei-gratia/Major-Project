from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.http import Http404
from ..mixins import GetSerializerClassMixin
from ..models import Program, SchoolLevel, Specialisation, Subject
from .serializers import SchoolLevelCreateSerializer, SpecialisationCreateSerializer, SubjectCreateSerializer, SubjectSerializer, \
    ProgramSerializer, SchoolLevelSerializer, SpecialisationSerializer, ProgramCreateSerializer


# ====== SCHOOL LEVEL VIEWSET ======
class SchoolLevelViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = SchoolLevel.objects.all()
    serializer_class = SchoolLevelSerializer
    serializer_action_classes = {
        'create': SchoolLevelCreateSerializer,
        'update': SchoolLevelCreateSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            SchoolLevel.objects.create(**validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.title = validated_data.get("title", instance.title)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'school level with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'school level deleted'}
        return Response(status=status.HTTP_204_NO_CONTENT)


# ====== SPECIALISATION VIEWSET ======
class SpecialisationViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Specialisation.objects.all()
    serializer_class = SpecialisationSerializer
    serializer_action_classes = {
        'create': SpecialisationCreateSerializer,
        'update': SpecialisationCreateSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            Specialisation.objects.create(**validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.title = validated_data.get("title", instance.title)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'specialisation with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'specialisation deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


# ====== PROGRAM VIEWSET ======
class ProgramViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    serializer_action_classes = {
        'create': ProgramCreateSerializer,
        'update': ProgramCreateSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            Program.objects.create(**validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.title = validated_data.get("title", instance.title)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'program with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        content = {'message: program deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


# ====== SUBJECT VIEWSET ======
class SubjectViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    serializer_action_classes = {
        'create': SubjectCreateSerializer,
        'update': SubjectCreateSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            Subject.objects.create(**validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.title = validated_data.get("title", instance.title)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'quiz with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'subject deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
