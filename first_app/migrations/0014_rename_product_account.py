# Generated by Django 4.1.7 on 2023-03-25 09:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first_app', '0013_telegramuser_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='Account',
        ),
    ]
