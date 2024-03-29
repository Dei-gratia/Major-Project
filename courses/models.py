from django.db import models
from main.fields import OrderField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
from users.models import User, Review
from main.models import Subject, SchoolLevel
from django.template.loader import render_to_string
from django.contrib.contenttypes import fields

# Create your models here.


# ====== COURSE MODEL ======
class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.SET_NULL, blank=True, null=True)
    school_level = models.ForeignKey(SchoolLevel,
                                     related_name='courses',
                                     on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(
        default='courses/images/default.png', upload_to='courses/images/')
    slug = models.SlugField(max_length=200,	unique=True)
    overview = models.TextField()
    total_ratings = models.FloatField(default=0.0)
    num_ratings = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    tags = models.TextField(blank=True)
    verified = models.IntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        User, related_name='courses_enrolled', blank=True)

    reviews = fields.GenericRelation(Review)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.average_rating = self.get_average_rating()
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_average_rating(self):
        if float(self.num_ratings) == 0.0 or float(self.total_ratings) == 0.0:
            return 0.000
        return round(float(self.total_ratings) / float(self.num_ratings), 3)


# ====== COURSE MODULE MODEL ======
class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    order = OrderField(blank=True,	for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


# ====== COURSE MODULE CONTENT MODEL ======
class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string('front/courses/content/{}.html'.format(
            self._meta.model_name),	{'item':	self})

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
