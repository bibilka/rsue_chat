from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from chat.forms import RegisterForm, LoginForm, InviteForm

# from chat.models import Friendship

# обработка 404
from chat.models import Profile


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>404 страница не найдена</h1>")

# приглашение друга
def invite(request):

    if not request.user.is_authenticated:
        return redirect('logout')

    if request.method != 'POST':
        return redirect('chat')

    form = InviteForm(request.POST)

    if form.is_valid():

        try:
            friend = User.objects.get(id=form.cleaned_data['friend'])

            if request.user.id == form.cleaned_data['friend']:
                form.add_error(None, 'Нельзя добавить в друзья самого себя.')

            elif request.user.profile.friends.filter(id=friend.id).exists():
                form.add_error(None, 'Вы уже дружите с ' + friend.username + '.')

            else:
                request.user.profile.friends.add(friend)
                friend.profile.friends.add(request.user)

                messages.add_message(request, messages.SUCCESS, 'Пользователь ' + friend.username + ' добавлен в ваши друзья!')
                return redirect('chat')

        except Exception as e:
            print(str(e))
            form.add_error(None, 'Произошла непредвиденная ошибка. Пожалуйста, обратитесь к администратору')

    return render(request, 'chat/room.html', {'form': form, 'id': request.user.id, 'nickname': request.user.username})

# чат
def chat(request):
    if request.user.is_authenticated:
        return render(request, 'chat/room.html', {'user': request.user})

    return redirect('auth')

# авторизация
def auth(request):

    if request.user.is_authenticated:
        return redirect('logout')

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            try:
                user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('chat')
                else:
                    form.add_error(None, 'Неверные данные!')
            except Exception as e:
                print(str(e))
                form.add_error(None, 'Ошибка при авторизации. Пожалуйста, обратитесь к администратору')

    return render(request, 'chat/auth.html', {'form': form})

# выход (деавторизация)
def logout(request):

    logout(request)
    return redirect('auth')

# регистрация
def register(request):
    if request.user.is_authenticated:
        return redirect('logout')

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.create(username=form.cleaned_data['username'])
                user.set_password(form.cleaned_data['password'])
                user.save()

                messages.add_message(request, messages.SUCCESS, "Вы успешно зарегистрировались! Можете войти.")
                return redirect('auth')
            except Exception as e:
                print(str(e))
                form.add_error(None, 'Ошибка при регистрации. Пожалуйста, обратитесь к администратору')

    return render(request, 'chat/register.html', {'form': form})
