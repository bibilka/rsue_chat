from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'display_friends')

    def display_friends(self, obj):
        return ', '.join([ friend.username for friend in obj.friends.all() ])
    display_friends.short_description = 'Друзья'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'chat', 'text', 'created_at', 'updated_at')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'display_users')

    def display_users(self, obj):
        return ', '.join([ profile.user.username for profile in obj.profiles.all() ])
    display_users.short_description = 'Пользователи'






