# Generated by Django 3.2.8 on 2021-12-22 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_auto_20211222_2150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverifytoken',
            options={'verbose_name': 'Токен', 'verbose_name_plural': 'Токены для подтверждения аккаунтов'},
        ),
        migrations.AlterField(
            model_name='emailverifytoken',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Подтвержден'),
        ),
    ]
