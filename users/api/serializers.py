from rest_framework import serializers
from ..models import Review, User, Profile


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.profile.profile_name')

    class Meta:
        model = Review
        fields = ['id', 'user', 'rate_value', 'comment', 'date']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id',	'email',	'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    user_id = serializers.CharField(source='user.id')

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'last_name',	'nickname',	'phone', 'gender', 'about',
                  'school_level', 'school', 'program', 'profile_completed', 'registration_tokens', 'image', 'updated']
