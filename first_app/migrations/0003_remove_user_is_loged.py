# Generated by Django 4.1.3 on 2022-12-11 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_user_is_loged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_loged',
        ),
    ]
