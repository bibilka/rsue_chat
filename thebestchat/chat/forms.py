from django import forms
from django.forms import PasswordInput

from .models import *

class RegisterForm(forms.Form):
    nickname = forms.CharField(max_length=100)
    password = forms.CharField(widget=PasswordInput())

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")

        if User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("Такой логин уже занят")
        return nickname