from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(EmailVerifyToken)
class AdminEmailVerifyToken(admin.ModelAdmin):
    list_display = ('id', 'email', 'token')

@admin.register(FriendRequest)
class AdminFriendRequest(admin.ModelAdmin):
    # административная модель для операций с заявками в друзья
    # поля: id, получатель, отправитель, дата создания
    list_display = ('id', 'request_sender', 'request_receiver', 'created_at')

    # фильтры по: получателю и отправителю
    list_filter = (
        ('request_sender', admin.RelatedOnlyFieldListFilter),
        ('request_receiver', admin.RelatedOnlyFieldListFilter),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # административная модель для операций с профилями пользователей
    # поля: id, пользователь, даты, друзья, аватар, чаты, заявки в друзья
    list_display = ('id', 'user', 'created_at', 'updated_at', 'display_friends', 'image_tag', 'chats_tag', 'friend_requests_tag', 'verified')
    fields = ('user', 'friends', 'avatar')

    # фильтры по пользователю
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
    )

    # отображаем список друзей через запятую
    def display_friends(self, obj):
        return ', '.join([ friend.username for friend in obj.friends.all() ])
    display_friends.short_description = 'Друзья'

    # превью аватарки
    def image_tag(self, obj):
        return format_html('<img height="35px" width="35px" src="{}" />'.format(obj.avatar.url)) if obj.avatar else ''
    image_tag.short_description = 'Аватарка'

    # чаты пользователя
    def chats_tag(self, obj):
        return format_html('<a href="/admin/chat/chat/?profiles__id__exact={}">{}</a>'.format(obj.id, Chat.objects.filter(profiles__id=obj.id).count()))
    chats_tag.short_description = 'Чаты'

    # заявки в друзья пользователя
    def friend_requests_tag(self, obj):
        return format_html('<a href="/admin/chat/friendrequest/?request_sender__id__exact={}">Отправленные</a> / <a href="/admin/chat/friendrequest/?request_receiver__id__exact={}">Необработанные</a>'.format(obj.id, obj.id))
    friend_requests_tag.short_description = 'Заявки в друзья'

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    # административная модель для операций с чатами
    # поля: id, название, даты, участники чата
    list_display = ('id', 'name', 'created_at', 'updated_at', 'display_users')

    # фильтр по участникам чата
    list_filter = (
        ('profiles', admin.RelatedOnlyFieldListFilter),
    )

    # отображаем список участнико чата через запятую
    def display_users(self, obj):
        return ', '.join([ profile.user.username for profile in obj.profiles.all() ])
    display_users.short_description = 'Пользователи'






