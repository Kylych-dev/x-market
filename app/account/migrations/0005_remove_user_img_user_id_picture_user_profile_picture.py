# Generated by Django 4.2.2 on 2023-07-17 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_blacklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='img',
        ),
        migrations.AddField(
            model_name='user',
            name='id_picture',
            field=models.ImageField(blank=True, null=True, upload_to='id_images/'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
