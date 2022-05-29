from django.db import models
from users.models import User
from main.models import SchoolLevel, Subject

# Create your models here.


class DiscussionTopic(models.Model):
    owner = models.ForeignKey(
        User, related_name='discussion_topics', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject,
                                related_name='discussion_topics',
                                on_delete=models.CASCADE)
    school_level = models.ForeignKey(SchoolLevel,
                                     related_name='discussion_topics',
                                     on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    cover_img = models.ImageField(
        upload_to='discussions/images/', default='discussions/images/topic_default.jpg')
    number_of_posts = models.IntegerField(default=0)

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}_{self.pk}'


class Post(models.Model):
    owner = models.ForeignKey(
        User, related_name='posts', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000)
    post_content = models.TextField(blank=True)
    discussion_topic = models.ForeignKey(
        DiscussionTopic, related_name='posts', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(
        upload_to="discussions/images/", default="discussions/images/default.png")

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}_post_{self.pk}'


class Replie(models.Model):
    user = models.ForeignKey(User, related_name='replies',
                             on_delete=models.SET_NULL, null=True, blank=True)
    replie_content = models.TextField()
    post = models.ForeignKey(
        Post, related_name='replies', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="discussions/images/", default="discussions/images/default.png")

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post}_reply_{self.user}_{self.pk}'
