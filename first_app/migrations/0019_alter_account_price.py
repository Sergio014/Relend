# Generated by Django 4.1.7 on 2023-04-05 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0018_account_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
