from django.db import models
from main.models import SchoolLevel, Subject
from users.models import User, Review
from main.fields import OrderField
from django.contrib.contenttypes import fields

# Create your models here.


class Quiz(models.Model):
    owner = models.ForeignKey(User,
                              related_name='quizzes_uploaded',
                              on_delete=models.SET_NULL, blank=True, null=True)

    subject = models.ForeignKey(Subject,
                                related_name='quizzes',
                                on_delete=models.SET_NULL, blank=True, null=True)
    school_level = models.ForeignKey(SchoolLevel,
                                     related_name='quizzes',
                                     on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=254)
    cover_img = models.ImageField(
        default='quizzes/images/default.jpg', upload_to='quizzes/images/')
    description = models.TextField(blank=True)
    number_of_questions = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    total_ratings = models.FloatField(default=0.0)
    num_ratings = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    tags = models.TextField(blank=True)
    verified = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now=True)

    reviews = fields.GenericRelation(Review)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def average_rating(self):
        if int(self.num_ratings) == 0 or float(self.total_ratings) == 0:
            return 0.000
        return round(float(self.total_ratings) / float(self.num_ratings), 3)


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=254, blank=True)
    option2 = models.CharField(max_length=254, blank=True)
    option3 = models.CharField(max_length=254, blank=True)
    option4 = models.CharField(max_length=254, blank=True)
    correct_option = models.CharField(max_length=254)

    order = OrderField(blank=True,	for_fields=['quiz'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.question)
