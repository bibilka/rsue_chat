from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from chat.forms import RegisterForm, LoginForm, InviteForm, ProfileSettingsForm
from chat.models import Profile, Chat, Message

from django.utils.timezone import localtime

# изменение настроек профиля
def profileSettings(request):
    if not request.user.is_authenticated:
        return redirect('logout')

    if request.method != 'POST':
        profile_settings_form = ProfileSettingsForm()
    else:
        profile_settings_form = ProfileSettingsForm(request.POST, request.FILES)
        if profile_settings_form.is_valid():

            password = profile_settings_form.cleaned_data.get("password")
            img = profile_settings_form.cleaned_data.get("avatar")
            if (password):
                user = request.user
                user.set_password(password)
                user.save()
                login(request, authenticate(request, username=user.username, password=password))

            profile = request.user.profile;
            profile.avatar = img
            profile.save()

            messages.add_message(request, messages.SUCCESS, 'Настройки успешно сохранены.')

        else:
            profile_settings_form.add_error(None, 'Произошла ошибка. Проверьте правильность введеных данных.')

    # получаем все чаты пользователя с последним сообщением
    chats = getChats(request)

    return render(request, 'chat/room.html', {'profile_settings_form': profile_settings_form, 'show_settings_form': True, 'user': request.user,'chats': chats})

# получение чатов пользователя
def getChats(request):
    chats = []
    for chat in Chat.objects.filter(profiles__id=request.user.profile.id):
        friend = chat.profiles.exclude(user_id=request.user.id).first()
        last_message = Message.objects.filter(chat_id=chat.id).order_by('-id').first()
        chats.append({
            'id': chat.id,
            'friend_name': friend.get_name(),
            'friend_avatar': friend.avatar.url if friend.avatar else '',
            'unreaded_messages': friend.messages(),
            'last_message': {
                'text': last_message.text,
                'time': localtime(last_message.created_at).time()
            }
        })
    return chats

# обработка 404
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
                # добавляем пользователей в друзья
                request.user.profile.friends.add(friend)
                friend.profile.friends.add(request.user)

                # создаем объект чата
                chat = Chat.objects.create(name=request.user.username+'/'+friend.username)
                chat.profiles.add(friend.profile)
                chat.profiles.add(request.user.profile)
                chat.save()

                messages.add_message(request, messages.SUCCESS, 'Пользователь ' + friend.username + ' добавлен в ваши друзья!')
                return redirect('chat')

        except Exception as e:
            print(str(e))
            form.add_error(None, 'Произошла непредвиденная ошибка. Пожалуйста, обратитесь к администратору')

    # получаем все чаты пользователя с последним сообщением
    chats = getChats(request)

    profile_settings_form = ProfileSettingsForm()

    return render(request, 'chat/room.html', {'form': form, 'profile_settings_form': profile_settings_form, 'id': request.user.id, 'nickname': request.user.username, 'chats': chats})

# чат
def chat(request):
    if request.user.is_authenticated:
        # получаем все чаты пользователя с последним сообщением
        chats = getChats(request)

        profile_settings_form = ProfileSettingsForm()

        return render(request, 'chat/room.html', {'user': request.user, 'show_chats': True, 'profile_settings_form': profile_settings_form, 'chats': chats})

    return redirect('auth')

# диалог
def dialog(request, chat_id):

    # проверям что юзер авторизован
    if not request.user.is_authenticated:
        return redirect('auth')

    # проверяем что этот чат юзера, а не чужой
    if not Chat.objects.filter(profiles__id=request.user.profile.id).filter(id=chat_id).exists():
        raise PermissionDenied()

    # получаем все чаты пользователя с последним сообщением
    chats = getChats(request)

    messages = Message.objects.filter(chat=chat_id)

    profile_settings_form = ProfileSettingsForm()

    return render(request, 'chat/room.html', {'chat': chat_id, 'show_chats': True, 'profile_settings_form': profile_settings_form, 'chats': chats, 'profile': request.user.profile.id, 'chatMessages': messages})

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
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

                messages.add_message(request, messages.SUCCESS, "Вы успешно зарегистрировались! Можете войти.")
                return redirect('auth')
            except Exception as e:
                print(str(e))
                form.add_error(None, 'Ошибка при регистрации. Пожалуйста, обратитесь к администратору')

    return render(request, 'chat/register.html', {'form': form})