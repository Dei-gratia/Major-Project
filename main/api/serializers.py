from rest_framework import serializers
from ..models import Subject, SchoolLevel, Program, Specialisation


# ====== SCHOOLLEVEL SERIALIZER ======
class SchoolLevelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolLevel
        fields = ['id',	'title']


class SchoolLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolLevel
        fields = ['id',	'title',	'slug']


# ====== SPECIALISATION SERIALIZER ======
class SpecialisationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialisation
        fields = ['id',	'title']


class SpecialisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialisation
        fields = ['id',	'title',	'slug']


# ====== PROGRAM SERIALIZER ======
class ProgramCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ['id',	'title']


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ['id',	'title',	'slug']


# ====== SUBJECT SERIALIZER ======
class SubjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id',	'title']


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id',	'title',	'slug']
