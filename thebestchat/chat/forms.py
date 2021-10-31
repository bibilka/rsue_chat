from django import forms
from django.core.validators import RegexValidator
from django.forms import PasswordInput

from .models import *

# форма приглашения друга
class InviteForm(forms.Form):
    friend = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super(InviteForm, self).clean()
        friend = cleaned_data.get('friend')

        if not User.objects.filter(id=friend).exists():
            raise forms.ValidationError("К сожалению, пользователя с таким ID не существует :c")


# форма регистрации
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

# форма авторизации
class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, required=True, label='Никнейм')
    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
