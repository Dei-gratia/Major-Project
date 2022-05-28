from django.db import models
from main.models import Subject, SchoolLevel
from users.models import User, Review
from django.contrib.contenttypes import fields

# Create your models here.


# ====== NOTEMODEL ======
class Note(models.Model):
    owner = models.ForeignKey(User,
                              related_name='notes_uploaded',
                              on_delete=models.SET_NULL, blank=True, null=True)
    school_level = models.ForeignKey(SchoolLevel,
                                     related_name='notes',
                                     on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey(Subject,
                                related_name='notes',
                                on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=254)
    cover_img = models.ImageField(
        default='notes/images/default.jpg', upload_to='notes/images/')
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/files/', blank=True)
    total_ratings = models.FloatField(max_length=254, default=0.0)
    num_ratings = models.CharField(max_length=254, default=0)
    downloads = models.CharField(max_length=254, default=0)
    tags = models.TextField(blank=True)
    verified = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now=True)

    reviews = fields.GenericRelation(Review)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def average_rating(self):
        if float(self.num_ratings) == 0.0 or float(self.total_ratings) == 0.0:
            return 0.000
        return round(float(self.total_ratings) / float(self.num_ratings), 3)
