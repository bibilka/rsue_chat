# Generated by Django 3.2.8 on 2021-12-15 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/profiles/'),
        ),
    ]
