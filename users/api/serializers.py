from rest_framework import serializers
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.profile.profile_name')

    class Meta:
        model = Review
        fields = ['id', 'user', 'rate_value', 'comment', 'date']
