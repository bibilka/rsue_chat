# Generated by Django 3.2.8 on 2021-12-15 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20211215_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]
