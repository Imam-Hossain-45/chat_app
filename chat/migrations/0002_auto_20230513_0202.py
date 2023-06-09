# Generated by Django 2.1.3 on 2023-05-13 02:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatwindow',
            options={'ordering': ['-id']},
        ),
        migrations.AlterUniqueTogether(
            name='chatwindow',
            unique_together={('user1', 'user2')},
        ),
    ]
