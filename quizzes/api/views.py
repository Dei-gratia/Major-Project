from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from main.mixins import GetSerializerClassMixin
from .serializers import QuizSerializer, QuizDetailSerializer, QuestionSerializer, QuizCreateSerializer, QuestionCreateSerializer
from ..models import Quiz, Question
from courses.models import Subject
from django.http import Http404


class QuizViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    serializer_action_classes = {
        'list': QuizSerializer,
        'create': QuizCreateSerializer,
        'update': QuizCreateSerializer,
    }

    filterset_fields = ("school_level", "subject",
                        "number_of_questions", "duration", "average_rating", )
    search_fields = ("title", "description", "questions", )
    ordering_fields = ("title", "average_rating", )
    ordering = ("-created", )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            Quiz.objects.create(owner=self.request.user, **validated_data)
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
            instance.number_of_questions = validated_data.get(
                "number_of_questions", instance.number_of_questions)
            instance.tags = validated_data.get("tags", instance.tags)
            instance.cover_img = validated_data.get(
                "cover_img", instance.cover_img)
            instance.duration = validated_data.get(
                "duration", instance.duration)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'message': 'quiz with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'quiz successfully deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


class QuestionViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    serializer_action_classes = {
        'create': QuestionCreateSerializer,
        'update': QuestionCreateSerializer,
    }

    filterset_fields = ("order", "correct_option")
    search_fields = ("question", "option1", "option2", "option3", "option4")
    ordering_fields = ("order", )
    ordering = ("order", )

    def get_queryset(self):
        print(self.kwargs)
        quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        return Question.objects.filter(quiz=quiz)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
            Question.objects.create(quiz=quiz, **validated_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            instance = self.get_object()
            instance.question = validated_data.get(
                "question", instance.question)
            instance.option1 = validated_data.get("option1", instance.option1)
            instance.option2 = validated_data.get("option2", instance.option2)
            instance.option3 = validated_data.get("option3", instance.option3)
            instance.option4 = validated_data.get("option4", instance.option4)
            instance.correct_option = validated_data.get(
                "correct_option", instance.correct_option)
            instance.order = validated_data.get("order", instance.order)

            instance.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            content = {'question': 'quiz with given id does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        content = {'message': 'question successfully deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
