from asyncore import read
from random import choices
from rest_framework import serializers
from ..models import Note
from users.models import Review
from courses.models import Subject
from users.api.serializers import ReviewSerializer


class NoteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['school_level', 'subject', 'title', 'cover_img',
                  'description', 'body', 'file', 'tags']


class NoteDetailSerializer(serializers.ModelSerializer):
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')
    downloads = serializers.IntegerField()
    #average_rating = serializers.FloatField(source='average_rating')
    created = serializers.DateTimeField(read_only=True)
    owner = serializers.CharField(source='owner.profile.profile_name')
    reviews = ReviewSerializer(many=True,	read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'school_level', 'subject', 'title', 'cover_img',
                  'description', 'body', 'file', 'average_rating',
                  'downloads', 'tags', 'created', 'owner', 'reviews']


class NoteSerializer(serializers.ModelSerializer):
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')
    average_rating = serializers.FloatField(source='num_ratings')
    created = serializers.DateTimeField()
    owner = serializers.CharField(source='owner.profile.profile_name')

    class Meta:
        model = Note
        fields = ['id', 'school_level', 'subject', 'title', 'cover_img',
                  'description', 'average_rating', 'created', 'owner']
