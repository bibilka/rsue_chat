from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.forms import PasswordInput, ModelForm

from .models import *

# форма приглашения друга
class InviteForm(forms.Form):
    # ID пользователя которому будет отправлена заявка
    friend = forms.IntegerField(required=True)

    # валидация формы
    def clean(self):
        cleaned_data = super(InviteForm, self).clean()
        friend = cleaned_data.get('friend')
        # проверяем существование пользователя
        if not User.objects.filter(id=friend).exists():
            raise forms.ValidationError("К сожалению, пользователя с таким ID не существует :c")


# форма регистрации
class RegisterForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']

    # поле никнейм и его правила валидации
    username = forms.CharField(min_length=3, max_length=10, required=True, label='Никнейм', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Может содержать только латинские буквы и цифры',
            code='invalid_username'
        ),
    ])
    username.group = 1

    # поле имя и его правила валидации
    first_name = forms.CharField(min_length=3, max_length=30, required=False, label='Имя', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])
    first_name.group = 2

    # поле фамилия и его правила валидации
    last_name = forms.CharField(min_length=3, max_length=30, required=False, label='Фамилия', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])
    last_name.group = 2

    # два поля под пароль (+ повтор пароля)
    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
    password.group = 1
    password_confirm = forms.CharField(widget=PasswordInput(), required=True, label='Повторите пароль')
    password.group = 1

    # поля, обязательные к заполнению
    def required_fields(self):
        return filter(lambda x: x.group == 1, self.fields.values())

    # поля, необязательные к заполнению
    def optional_fields(self):
        return filter(lambda x: x.group == 2, self.fields.values())

    # валидация формы
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

    # поле для изменения пароля
    password = forms.CharField(widget=PasswordInput(), min_length=3, max_length=30, required=True, label='Пароль')

    # поле для измненения имени и его правила валидации
    first_name = forms.CharField(min_length=3, max_length=30, required=False, label='Имя', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])

    # поле для измненения фамилии и его правила валидации
    last_name = forms.CharField(min_length=3, max_length=30, required=False, label='Фамилия', validators=[
        RegexValidator(
            regex='^[а-яА-Яa-zA-Z\s]{3,30}$',
            message='Проверьте правильность введенных данных',
            code='invalid_name'
        )
    ])

    # поля для загрузки (или изменения) аватарки профиля
    avatar = forms.ImageField(required=False)
