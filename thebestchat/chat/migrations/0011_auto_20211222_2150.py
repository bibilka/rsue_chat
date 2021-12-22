# Generated by Django 3.2.8 on 2021-12-22 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_auto_20211222_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverifytoken',
            name='profile',
        ),
        migrations.AddField(
            model_name='emailverifytoken',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='Сообщение'),
        ),
    ]