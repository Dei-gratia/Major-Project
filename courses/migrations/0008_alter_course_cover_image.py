# Generated by Django 4.0.4 on 2022-06-04 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cover_image',
            field=models.ImageField(default='courses/images/default.png', upload_to='courses/images/'),
        ),
    ]