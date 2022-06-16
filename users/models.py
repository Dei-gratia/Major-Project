import profile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from phone_field import PhoneField
from django.utils.text import slugify
from main.models import SchoolLevel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


# ======USER MODEL======
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        ordering = ['email']


# ======PROFILE MODEL======
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    profile_name = models.CharField(
        max_length=254, blank=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateTimeField(max_length=50, blank=True, null=True)
    about = models.CharField(max_length=254, blank=True)
    school_level = models.ForeignKey(
        SchoolLevel, related_name='students', on_delete=models.SET_NULL, null=True, blank=True)
    program = models.CharField(max_length=254, blank=True)
    school = models.CharField(max_length=254, blank=True)
    profile_completed = models.IntegerField(default=0)
    image = models.ImageField(default='profilepics/default.png',
                              upload_to=f'profilepics/')
    updated = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.profile_name:
            profile_name = ""
            if self.user.first_name:
                profile_name = self.user.first_name.replace(
                    " ", "")
            if self.user.last_name:
                profile_name += self.user.last_name.replace(
                    " ", "")
            if profile_name:
                self.profile_name = profile_name
        if not self.about:
            if self.profile_name:
                self.about = f"I am {self.profile_name}"
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} profile'


# ====== RATING MODEL ======
class Review(models.Model):
    user = models.ForeignKey(User,
                             related_name='reviews_given',
                             on_delete=models.SET_NULL, blank=True, null=True)
    rate_value = models.CharField(max_length=254)
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'note',
                                         'quiz',
                                         'course',)})
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rate_value} {self.comment}'
