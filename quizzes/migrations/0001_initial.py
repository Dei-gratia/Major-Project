# Generated by Django 4.0.4 on 2022-05-28 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_program_specialisation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('cover_img', models.ImageField(default='quizzes/images/default.jpg', upload_to='quizzes/images/')),
                ('description', models.TextField(blank=True)),
                ('number_of_questions', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('total_ratings', models.IntegerField(default=0)),
                ('num_ratings', models.IntegerField(default=0)),
                ('attempts', models.IntegerField(default=0)),
                ('tags', models.TextField(blank=True)),
                ('verified', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes_uploaded', to=settings.AUTH_USER_MODEL)),
                ('school_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes', to='main.schoollevel')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes', to='main.subject')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option1', models.CharField(blank=True, max_length=254)),
                ('option2', models.CharField(blank=True, max_length=254)),
                ('option3', models.CharField(blank=True, max_length=254)),
                ('option4', models.CharField(blank=True, max_length=254)),
                ('correct_option', models.CharField(max_length=254)),
                ('order', main.fields.OrderField(blank=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizzes.quiz')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
