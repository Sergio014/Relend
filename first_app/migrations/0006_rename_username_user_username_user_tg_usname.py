# Generated by Django 4.1.3 on 2022-12-26 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0005_product_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Username',
            new_name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='tg_usname',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
