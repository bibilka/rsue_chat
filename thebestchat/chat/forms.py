from django import forms
from django.core.validators import RegexValidator
from django.forms import PasswordInput
from django.contrib.auth.models import User

from .models import *

class RegisterForm(forms.Form):

    username = forms.CharField(max_length=10, required=True, label='Никнейм', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Может содержать только буквы и цифры',
            code='invalid_username'
        ),
    ])
    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
    password_confirm = forms.CharField(widget=PasswordInput(), required=True, label='Повторите пароль')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # валидация паролей
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                {'password_confirm': "Пароли не совпадают", 'password': ''}
            )
        # валидация никнейма
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': "Такой логин уже занят"})

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, required=True, label='Никнейм')
    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
