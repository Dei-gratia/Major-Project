# Generated by Django 4.0.4 on 2022-06-18 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0006_remove_discussiontopic_number_of_posts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiontopic',
            name='verified',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='verified',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='replie',
            name='verified',
            field=models.IntegerField(default=1),
        ),
    ]
