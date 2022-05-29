from rest_framework import serializers
from ..models import DiscussionTopic, Replie, Post
from users.models import User


class ReplieCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Replie
        fields = ['id',	'replie_content', 'image']


class ReplieSerializer(serializers.ModelSerializer):
    replier = serializers.CharField(source='user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data['replier'])
        if not data['replier']:
            data['replier'] = "anonymous"
        else:
            data['replier'] = User.objects.get(
                email=data['replier']).profile.profile_name
        return data

    class Meta:
        model = Replie
        fields = ['id',	'replie_content', 'replier', 'image', 'date']


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'post_content', 'image']


class PostDetailSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='owner')
    replies = ReplieSerializer(many=True, read_only=True)
    total_replies = serializers.SerializerMethodField(read_only=True)

    def get_total_replies(self, discussion_topic):
        return discussion_topic.replies.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['poster']:
            data['poster'] = "anonymous"
        else:
            data['poster'] = User.objects.get(
                email=data['poster']).profile.profile_name
        return data

    class Meta:
        model = Post
        fields = ['id', 'title', 'post_content', 'poster',
                  'image', 'date', 'total_replies', 'replies']


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='owner')
    total_replies = serializers.SerializerMethodField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['poster']:
            data['poster'] = "anonymous"
        else:
            data['poster'] = User.objects.get(
                email=data['poster']).profile.profile_name
        return data

    def get_total_replies(self, discussion_topic):
        return discussion_topic.replies.count()

    class Meta:
        model = Post
        fields = ['id', 'discussion_topic', 'title',
                  'post_content', 'poster', 'image', 'date', 'total_replies']


class TopicCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscussionTopic
        fields = ['id', 'school_level', 'subject',
                  'title', 'cover_img', ]


class TopicDetailSerializer(serializers.ModelSerializer):
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')
    created_by = serializers.CharField(source='owner')
    posts = PostSerializer(many=True, read_only=True)
    total_posts = serializers.SerializerMethodField(read_only=True)

    def get_total_posts(self, discussion_topic):
        return discussion_topic.posts.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data['created_by'])
        if not data['created_by']:
            data['created_by'] = "anonymous"
        else:
            data['created_by'] = User.objects.get(
                email=data['created_by']).profile.profile_name
        return data

    class Meta:
        model = DiscussionTopic
        fields = ['id', 'school_level', 'subject', 'title', 'cover_img',
                  'created_by', 'date', 'total_posts',  'posts']


class TopicSerializer(serializers.ModelSerializer):
    school_level = serializers.CharField(source='school_level.title')
    subject = serializers.CharField(source='subject.title')
    created_by = serializers.CharField(source='owner')
    total_posts = serializers.SerializerMethodField(read_only=True)

    def get_total_posts(self, discussion_topic):
        return discussion_topic.posts.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['created_by']:
            data['created_by'] = "anonymous"
        else:
            data['created_by'] = User.objects.get(
                email=data['created_by']).profile.profile_name
        return data

    class Meta:
        model = DiscussionTopic
        fields = ['id', 'school_level', 'subject', 'title', 'cover_img',
                  'created_by', 'date', 'total_posts']
