from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint

# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    friends = models.ManyToManyField(User, blank=True, related_name='friends', verbose_name='Друзья')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    chats = models.ManyToManyField('Chat', related_name='chats')
    avatar = models.ImageField(null=True, blank=True, upload_to='images/profiles/')

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete()
        except:
            pass
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Список профилей'

    def __str__(self):
        return self.user.username

    def get_name(self):
        if (self.user.first_name or self.user.last_name):
            return self.user.get_full_name
        else:
            return self.user.username

    @staticmethod
    def messages():
        # todo: заглушка (кол-во непрочитанных сообщений)
        return str(randint(0, 100))

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

# Чат
class Chat(models.Model):
    name = models.CharField(max_length=100, verbose_name="Чат")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    profiles = models.ManyToManyField(Profile, related_name='profiles')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return self.name

# Сообщение в чате
class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Отправитель")
    chat = models.ForeignKey('Chat', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Чат")
    text = models.CharField(max_length=255, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text

