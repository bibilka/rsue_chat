# Generated by Django 3.2.8 on 2021-12-22 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_message_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='EmailVerifyToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='chat.profile', verbose_name='Отправитель')),
            ],
        ),
    ]
