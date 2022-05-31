# Generated by Django 4.0.4 on 2022-05-30 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_note_num_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='num_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='note',
            name='total_ratings',
            field=models.FloatField(default=0.0),
        ),
    ]
