from django.db import models
from phone_field import PhoneField
from django.utils.text import slugify


# Create your models here.


# ======HOME MODEL=======
class Home(models.Model):
    banner_txt = models.CharField(max_length=254)
    slider1_txt = models.CharField(max_length=254)
    tags = models.TextField()
    footer_abt_txt = models.TextField()

    updated = models.DateTimeField(auto_now=True)

    def tags_list(self):
        return self.tags.split(',')

    def __str__(self):
        return f'{self.banner_txt}'


class HomeImage(models.Model):
    home = models.ForeignKey(
        Home, related_name='images', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='home/images/')
    img_heading_txt = models.CharField(max_length=254, blank=True)
    img_txt = models.TextField(blank=True)


# ======ABOUT MODEL======
class About(models.Model):
    heading = models.CharField(max_length=254)
    about_txt = models.TextField()

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading


class AboutImage(models.Model):
    about = models.ForeignKey(
        About, related_name='images', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='about/images/')
    img_txt = models.CharField(max_length=254, default=img.name, blank=True)


class Address(models.Model):
    about = models.ForeignKey(
        About, related_name='addresses', on_delete=models.CASCADE)
    address = models.CharField(max_length=254)


class Email(models.Model):
    about = models.ForeignKey(
        About, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    primary = models.BooleanField()


class Phone(models.Model):
    about = models.ForeignKey(
        About, related_name='phone_numbers', on_delete=models.CASCADE)
    phone = PhoneField()
    primary = models.BooleanField()


class Social(models.Model):
    about = models.ForeignKey(
        About, related_name='socials', on_delete=models.CASCADE)
    social_name = models.CharField(max_length=254)
    display_title = models.CharField(max_length=254, default='connect with us')
    link = models.URLField(max_length=500, default='#')
    social_font_owesome_icon = models.CharField(max_length=254, blank=True)


# ======CONTACT SECTION======
class Contact(models.Model):
    name = models.CharField(max_length=254, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    message = models.TextField(blank=True)
    seen = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


# ======SUBSCRIBE SECTION======
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"


# ======SCHOOL LEVEL MODEL======
class SchoolLevel(models.Model):
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254,	unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(SchoolLevel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


# ======SPECIALISATION MODEL======
class Specialisation(models.Model):
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254,	unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Specialisation, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


# ====== PROGRAM MODEL======
class Program(models.Model):
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254,	unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Program, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


# ======SUBJECT MODEL======
class Subject(models.Model):
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254,	unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
