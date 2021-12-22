from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from encrypted_model_fields.fields import EncryptedCharField

# Профиль пользователя
class Profile(models.Model):
    # пользователь (представлено как связь один к одному с базовой Django-моделью пользователя)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    # друзья (поле представлено в виде связи многие ко многим с другими пользователям)
    friends = models.ManyToManyField(User, blank=True, related_name='friends', verbose_name='Друзья')
    # даты создания и изменения
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    # чаты (представлено в виде связи многие ко многим с моделью чаты)
    chats = models.ManyToManyField('Chat', related_name='chats')
    # аватар профиля
    avatar = models.ImageField(null=True, blank=True, upload_to='images/profiles/')
    # подтвержден ли пользователь
    verified = models.BooleanField(default=False, verbose_name='Подтвержден')

    # расширяем метод сохранения модели
    def save(self, *args, **kwargs):
        try:
            # если аватар был обновлен - удаляем старую картинку из файлового хранилища
            this = Profile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete()
        except:
            pass
        super(Profile, self).save(*args, **kwargs)

    # отображаемые локализированные названия модели
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Список профилей'

    # преобразование объекта модели к строке
    def __str__(self):
        return self.user.username

    # метод получения имени (если есть фамилия или имя - выводим их, иначе никнейм)
    def get_name(self):
        if (self.user.first_name or self.user.last_name):
            return self.user.get_full_name
        else:
            return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        # при создании объекта модели пользователя - создаем объект модели профиль
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        # при обновлении объекта модели пользователя - обновляем объект модели профиль
        instance.profile.save()

# заявка в друзья
class FriendRequest(models.Model):
    # отправитель заявки (представлено в виде связи с профилем)
    request_sender = models.ForeignKey('Profile', on_delete=models.PROTECT, verbose_name="Отправитель", related_name='request_sender_profile')
    # получатель заявки (представлено в виде связи с профилем)
    request_receiver = models.ForeignKey('Profile', on_delete=models.PROTECT, verbose_name="Получатель", related_name='request_receiver_profile')
    # дата создания заявки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    # отображаемые локализированные названия модели
    class Meta:
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'

# Чат
class Chat(models.Model):
    # название чата (для удобства визуальной идентификации)
    name = models.CharField(max_length=100, verbose_name="Чат")
    # даты создания и обновления
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    # участники чата (представлено как связь многие ко многим с моделью профиля)
    profiles = models.ManyToManyField(Profile, related_name='profiles')

    # отображаемые локализированные названия модели
    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    # преобразование объекта модели к строке
    def __str__(self):
        return self.name

# токены для подтверждения email
class EmailVerifyToken(models.Model):
    email = models.EmailField(verbose_name="Email", default="")
    token = models.CharField(max_length=100)

    # отображаемые локализированные названия модели
    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены для подтверждения аккаунтов'

# Сообщение в чате
class Message(models.Model):
    # отправитель (представлено как связь с моделью профиля)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Отправитель")
    # указатель на чат (представлено в виде связи с моделью чата)
    chat = models.ForeignKey('Chat', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Чат")
    # текст сообщения (в базе данных хранится в зашифрованном виде)
    text = EncryptedCharField(max_length=255, verbose_name="Сообщение")
    # даты создания и изменения
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    # флаг указатель - было ли сообщение прочитано
    was_read = models.BooleanField(default=False)

    # отображаемые локализированные названия модели
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    # преобразование объекта модели к строке
    def __str__(self):
        return self.text

    # сокращенный вариант сообщения (для вывода последнего сообщения в диалоге)
    def get_short_text(self):
        if len(self.text) > 20:
            return self.text[:20] + "..."
        else:
            return self.text