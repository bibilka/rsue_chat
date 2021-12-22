from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from chat.forms import RegisterForm, LoginForm, InviteForm, ProfileSettingsForm
from chat.models import Profile, Chat, Message, FriendRequest, EmailVerifyToken

from django.utils.timezone import localtime
from uuid import uuid4

from django.core.mail import EmailMessage

from django.db import transaction

# активные заявки в друзья
def getFriendRequests(request):

    # отправленные заявки текущего пользователя (исходящие)
    posted_requests = []
    for posted_request in FriendRequest.objects.filter(request_sender_id=request.user.profile.id):
        posted_requests.append({
            'id': posted_request.id,
            'sender': request.user.profile,
            'receiver': Profile.objects.get(id=posted_request.request_receiver_id),
            'datetime': posted_request.created_at
        })

    # активные запросы в друзья для текущего пользователя (входящие)
    incoming_requests = []
    for incoming_request in FriendRequest.objects.filter(request_receiver_id=request.user.profile.id):
        incoming_requests.append({
            'id': incoming_request.id,
            'sender': Profile.objects.get(id=incoming_request.request_sender_id),
            'receiver': request.user.profile,
            'datetime': incoming_request.created_at
        })
    return {'posted_requests': posted_requests, 'incoming_requests': incoming_requests}

# обработка заявки в друзья
def processFriendRequest(request):
    # проверка авторизации
    if not request.user.is_authenticated:
        return redirect('logout')

    # проверка метода отправки формы
    if request.method != 'POST':
        return redirect('chat')

    # проверяем наличие обрабатываемого запроса в друзья в базе данных
    friend_request = get_object_or_404(FriendRequest, pk=request.POST.get('request_id'))

    # если заявка была принята
    if request.POST.get('action') == 'accept':
        # добавляем пользователей в друзья
        friend = Profile.objects.get(id=friend_request.request_sender_id)
        request.user.profile.friends.add(friend.user)
        friend.friends.add(request.user)

        # создаем объект чата
        chat = Chat.objects.create(name=request.user.username + '/' + friend.user.username)
        chat.profiles.add(friend)
        chat.profiles.add(request.user.profile)
        chat.save()

        messages.add_message(request, messages.SUCCESS, 'Пользователь ' + friend.user.username + ' добавлен в ваши друзья!')

    # удаляем заявку
    friend_request.delete()

    # возвращаем на главную страницу чата
    return redirect('chat')

# отправка заявки в друзья
def sendFriendRequest(request):
    # проверка авторизации
    if not request.user.is_authenticated:
        return redirect('logout')

    # проверка метода отправки формы
    if request.method != 'POST':
        return redirect('chat')

    # инициализируем объект формы и заполянем данными из POST запроса
    inviteForm = InviteForm(request.POST)

    # валидируем форму
    if inviteForm.is_valid():
        try:
            friend = User.objects.get(id=inviteForm.cleaned_data['friend'])

            if request.user.id == inviteForm.cleaned_data['friend']:
                inviteForm.add_error(None, 'Нельзя добавить в друзья самого себя.')

            elif request.user.profile.friends.filter(id=friend.id).exists():
                inviteForm.add_error(None, 'Вы уже дружите с ' + friend.username + '.')

            elif (FriendRequest.objects.filter(request_sender_id=friend.profile.id, request_receiver_id=request.user.profile.id).exists()
                  or FriendRequest.objects.filter(request_sender_id=request.user.profile.id, request_receiver_id=friend.profile.id).exists()):
                inviteForm.add_error(None, 'Такая заявка уже существует.')

            else:
                # создаем заявку
                FriendRequest.objects.create(request_sender_id=request.user.profile.id, request_receiver_id=friend.profile.id)
                messages.add_message(request, messages.SUCCESS, 'Вы отправили заявку в друзья пользователю ' + friend.username + '!')

        except Exception as e:
            print(str(e))
            inviteForm.add_error(None, 'Произошла непредвиденная ошибка. Пожалуйста, обратитесь к администратору')

    # получаем все чаты пользователя с последним сообщением
    chats = getChats(request)
    # получаем все заявки в друзья текущего пользователя
    friend_requests = getFriendRequests(request)
    # форма настроек профиля
    profile_settings_form = ProfileSettingsForm()

    return render(request, 'chat/room.html', {
        'inviteForm': inviteForm,
        'profile_settings_form': profile_settings_form,
        'user': request.user,
        'show_friends': True,
        'chats': chats,
        'friend_requests': friend_requests
    })

# изменение настроек профиля
def profileSettings(request):

    # проверка авторизации
    if not request.user.is_authenticated:
        return redirect('logout')

    # проверка метода отправки формы
    if request.method != 'POST':
        profile_settings_form = ProfileSettingsForm()

    else:
        # если форма была отправлена - инициализируем объект, заполняем данными из POST запроса и получаем переданные файлы
        profile_settings_form = ProfileSettingsForm(request.POST, request.FILES)
        if profile_settings_form.is_valid():
            # валидируем форму
            password = profile_settings_form.cleaned_data.get("password")
            img = profile_settings_form.cleaned_data.get("avatar")

            user = request.user
            user.first_name = profile_settings_form.cleaned_data.get("first_name", "")
            user.last_name = profile_settings_form.cleaned_data.get("last_name", "")

            # изменяем пароль, только если пришел новый пароль
            if (password and password!='password'):
                user.set_password(password)

            # сохраняем данные пользователя и авторизуем передавая обновленный объект модели
            user.save()
            login(request, authenticate(request, username=user.username, password=password))

            # сохраняем аватарку
            profile = request.user.profile;
            profile.avatar = img
            profile.save()

            messages.add_message(request, messages.SUCCESS, 'Настройки успешно сохранены.')

        else:
            profile_settings_form.add_error(None, 'Произошла ошибка. Проверьте правильность введеных данных.')

    # получаем все чаты пользователя с последним сообщением
    chats = getChats(request)
    # получаем все заявки в друзья текущего пользователя
    friend_requests = getFriendRequests(request)

    return render(request, 'chat/room.html', {
        'profile_settings_form': profile_settings_form,
        'show_settings_form': True,
        'user': request.user,
        'chats': chats,
        'friend_requests': friend_requests
    })

# получение чатов текущего пользователя
def getChats(request):
    chats = []
    for chat in Chat.objects.filter(profiles__id=request.user.profile.id):
        # пользователь с которым ведется диалог
        friend = chat.profiles.exclude(user_id=request.user.id).first()
        # последнее сообщение
        last_message = Message.objects.filter(chat_id=chat.id).order_by('-id').first()
        chats.append({
            'id': chat.id,
            'friend_name': friend.get_name(),
            # аватарка
            'friend_avatar': friend.avatar.url if friend.avatar else '',
            # кол-во непрочитанных сообщений
            'unreaded_messages': Message.objects.filter(chat_id=chat.id, profile_id=friend, was_read=False).count(),
            # текст и время отправки последнего сообщения
            'last_message': {
                'text':   last_message.get_short_text() if last_message else '',
                'time': localtime(last_message.created_at).time() if last_message else '',
            }
        })
    return chats

# обработка 404
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>404 страница не найдена</h1>")

# главная страница чата (список диалогов)
def chat(request):

    if request.user.is_authenticated:
        # получаем все чаты пользователя с последним сообщением
        chats = getChats(request)
        # получаем все заявки в друзья текущего пользователя
        friend_requests = getFriendRequests(request)
        # форма настроек профиля
        profile_settings_form = ProfileSettingsForm()

        return render(request, 'chat/room.html', {
            'user': request.user,
            'show_chats': True,
            'profile_settings_form': profile_settings_form,
            'chats': chats,
            'friend_requests': friend_requests
        })
    # если не авторизован - отправляем на страницу входа
    return redirect('auth')

# отображение страницы конкретного диалога
def dialog(request, chat_id):

    # проверям что юзер авторизован
    if not request.user.is_authenticated:
        return redirect('auth')

    # проверяем что этот чат юзера, а не чужой
    if not Chat.objects.filter(profiles__id=request.user.profile.id).filter(id=chat_id).exists():
        raise PermissionDenied()

    # получаем сообщения в диалоге
    messages = Message.objects.filter(chat=chat_id)

    # заявки в друзья и форма настроек профиля
    friend_requests = getFriendRequests(request)
    profile_settings_form = ProfileSettingsForm()

    # помечаем все сообщения прочитанными
    messages.update(was_read=True)

    # получаем все чаты пользователя с последним сообщением
    chats = getChats(request)

    return render(request, 'chat/room.html', {
        'chat': chat_id,
        'show_chats': True,
        'profile_settings_form': profile_settings_form,
        'chats': chats,
        'profile': request.user.profile.id,
        'chatMessages': messages,
        'friend_requests': friend_requests
    })

# авторизация
def auth(request):

    # если юзер уже авторизован - выходим
    if request.user.is_authenticated:
        return redirect('logout')

    # инициализируем объект формы
    form = LoginForm()

    if request.method == 'POST':
        # если форма была отправлена - заполняем объект данным из POST запроса
        form = LoginForm(request.POST)

        if form.is_valid():
            # валидируем форму
            try:
                # если юзер ввел правильные логин и пароль - авторизуем
                user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    if get_object_or_404(Profile, user_id=user.id).verified:
                        login(request, user)
                        # и отправляем на страницу чатов
                        return redirect('chat')
                    else:
                        form.add_error(None, 'Вы не подтвердили аккаунт.')
                else:
                    form.add_error(None, 'Неверные данные!')
            except Exception as e:
                print(str(e))
                form.add_error(None, 'Ошибка при авторизации. Пожалуйста, обратитесь к администратору')

    # иначе отображаем страницу с авторизацией
    return render(request, 'chat/auth.html', {'form': form})

# выход (деавторизация)
def logout(request):
    logout(request)
    return redirect('auth')

# регистрация
def register(request):
    # если юзер уже авторизован - выходим
    if request.user.is_authenticated:
        return redirect('logout')

    # инициализируем объект формы
    form = RegisterForm()

    if request.method == 'POST':
        # если форма была отправлена - получаем данные из POST запроса
        form = RegisterForm(request.POST)

        if form.is_valid():
            # валидируем форму
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()

                    # отправляем письмо для подтверждения
                    send_registration_email(request, user.email)

                    # создаем нового пользователя и делаем редирект на страницу авторизации
                    messages.add_message(request, messages.SUCCESS, "Вы успешно зарегистрировались! Проверьте свою почту.")
                    return redirect('auth')
            except Exception as e:
                print(str(e))
                form.add_error(None, 'Ошибка при регистрации. Пожалуйста, обратитесь к администратору')
    # иначе отображаем страницу регистрации
    return render(request, 'chat/register.html', {'form': form})

# подтверждение пользователя по email адресу
def verify_email(request):

    # валидируем запрос
    if request.method != 'GET' or 'token' not in request.GET or 'email' not in request.GET:
        raise PermissionDenied()

    # получаем объекты токена и профиля
    email_verify_object = get_object_or_404(EmailVerifyToken, email=request.GET['email'], token=request.GET['token'])
    profile = get_object_or_404(Profile, user__email=request.GET['email'])

    with transaction.atomic():
        # подтверждаем профиль и удаляем объект токена
        profile.verified = True
        profile.save()

        email_verify_object.delete()

    # перенаправляем на страницу авторизации
    messages.add_message(request, messages.SUCCESS, "Аккаунт подтвержден! Можете войти.")
    return redirect('auth')

# отправка письма на почту пользователю для подтверждения аккаунта
def send_registration_email(request, email_to):

    # генерируем уникальный токен
    token = uuid4()
    EmailVerifyToken.objects.create(email=email_to, token=token)

    # отправляем письмо
    email = EmailMessage(
        'Регистрация на платформе The Best Chat',
        'Подтвердите регистрацию, перейдя по ссылке: ' + request.build_absolute_uri('/chat/verify-email?token={}&email={}'.format(token, email_to)),
        to=[email_to]
    )
    email.send()
