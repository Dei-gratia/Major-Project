# Generated by Django 4.0.4 on 2022-05-28 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_rename_uploader_note_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='total_ratings',
            field=models.FloatField(default=0.0, max_length=254),
        ),
    ]