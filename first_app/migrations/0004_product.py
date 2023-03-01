# Generated by Django 4.1.3 on 2022-12-12 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_remove_user_is_loged'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(null=True, upload_to='images/', verbose_name='')),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('info', models.CharField(max_length=1000)),
                ('price', models.CharField(max_length=10)),
            ],
        ),
    ]