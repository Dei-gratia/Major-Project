# Generated by Django 4.0.4 on 2022-05-29 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_program_specialisation'),
        ('discussions', '0003_rename_reply_content_replie_replie_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussiontopic',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussion_topics', to='main.subject'),
        ),
    ]
