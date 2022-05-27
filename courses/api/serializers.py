from rest_framework import serializers
from ..models import Course, Module, Content, ItemBase


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ['id', 'order',	'title',	'description']


class CourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['school_level', 'subject', 'title',	'overview']


class CourseDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.profile.profile_name')
    modules = ModuleSerializer(many=True, read_only=True)
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')

    class Meta:
        model = Course
        fields = ['id',	'school_level', 'subject', 'title',	'slug',	'overview',
                  'created', 'owner', 'modules']


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.profile.profile_name')
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')

    class Meta:
        model = Course
        fields = ['id',	'school_level', 'subject', 'title',	'slug',	'overview',
                  'created', 'owner', ]


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self,	value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title',	'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)
    subject = serializers.CharField(source='subject.title')
    school_level = serializers.CharField(source='school_level.title')

    class Meta:
        model = Course
        fields = ['id', 'school_level',	'subject', 'title', 'slug',
                  'overview',	'created', 'owner',	'modules']
