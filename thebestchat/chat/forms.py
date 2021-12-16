from django import forms
from django.core.validators import RegexValidator
from django.forms import PasswordInput, ModelForm

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
class RegisterForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']

    username = forms.CharField(min_length=3, max_length=10, required=True, label='Никнейм', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Может содержать только латинские буквы и цифры',
            code='invalid_username'
        ),
    ])
    username.group = 1

    first_name = forms.CharField(min_length=3, max_length=30, required=False, label='Имя', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])
    first_name.group = 2

    last_name = forms.CharField(min_length=3, max_length=30, required=False, label='Фамилия', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])
    last_name.group = 2

    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
    password.group = 1
    password_confirm = forms.CharField(widget=PasswordInput(), required=True, label='Повторите пароль')
    password.group = 1

    def required_fields(self):
        return filter(lambda x: x.group == 1, self.fields.values())

    def optional_fields(self):
        return filter(lambda x: x.group == 2, self.fields.values())

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

# форма настроек пользователя
class ProfileSettingsForm(forms.Form):
    password = forms.CharField(widget=PasswordInput(), min_length=3, max_length=30, required=True, label='Пароль')
    first_name = forms.CharField(min_length=3, max_length=30, required=False, label='Имя', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])
    last_name = forms.CharField(min_length=3, max_length=30, required=False, label='Фамилия', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])
    avatar = forms.ImageField(required=False)
