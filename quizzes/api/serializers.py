from rest_framework import serializers
from ..models import Quiz, Question
from users.api.serializers import ReviewSerializer


class QuestionCreateSerializer(serializers.ModelSerializer):
    correct_option = serializers.ChoiceField(choices=[1, 2, 3, 4])

    class Meta:
        model = Question
        fields = ['id',	'question', 'option1', 'option2',
                  'option3', 'option4', 'correct_option', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    correct_option = serializers.ChoiceField(choices=[1, 2, 3, 4])

    class Meta:
        model = Question
        fields = ['id',	'question', 'option1', 'option2',
                  'option3', 'option4', 'correct_option', 'order']


class QuizCreateSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField()

    class Meta:
        model = Quiz
        fields = ['school_level', 'subject', 'title', 'cover_img',
                  'description', 'number_of_questions', 'duration', 'tags']


class QuizDetailSerializer(serializers.ModelSerializer):
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')
    owner = serializers.CharField(source='owner.profile.profile_name')
    questions = QuestionSerializer(many=True,	read_only=True)
    reviews = ReviewSerializer(many=True,	read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'school_level', 'subject', 'title', 'cover_img',
                  'description', 'number_of_questions', 'duration', 'average_rating',
                  'attempts', 'tags', 'created', 'owner', 'questions', 'reviews']


class QuizSerializer(serializers.ModelSerializer):
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')
    created = serializers.DateTimeField()
    owner = serializers.CharField(source='owner.profile.profile_name')

    class Meta:
        model = Quiz
        fields = ['id', 'school_level', 'subject', 'title', 'cover_img',
                  'description', 'number_of_questions', 'duration', 'average_rating',
                  'created', 'owner']
