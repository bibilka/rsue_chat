from django.db.models import Model
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from chat.forms import RegisterForm
from chat.models import User, Message


# Create your views here.
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Ты куда звонишь? Сынок ты ебаный.</h1>")

def user(request, id):

    user = get_object_or_404(User, pk=id)

    return render(request, 'chat/user.html', {'user': user})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create(**form.cleaned_data)
                return HttpResponse("Успешная регистрация.")
            except:
                form.add_error(None, 'Ошибка при регистрации')
        else:
            form.add_error(None, 'Ошибка при регистрации')
    else:
        form = RegisterForm()
    return render(request, 'chat/register.html', {'form': form})


def chat(request):
    return render(request, 'chat/room.html')

    # Показ последних 10 сообщений
    # chat_queryset = Message.objects.order_by("-created_at")[:10]
    # chat_message_count = len(chat_queryset)
    # if chat_message_count > 0:
    #     first_message_id = chat_queryset[len(chat_queryset) - 1].id
    # else:
    #     first_message_id = -1
    # previous_id = -1
    # if first_message_id != -1:
    #     try:
    #         previous_id = Message.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
    #     except IndexError:
    #         previous_id = -1
    # chat_messages = reversed(chat_queryset)
    #
    # return render(request, "chat/room.html", {
    #     'chat_messages': chat_messages,
    #     'first_message_id': previous_id,
    # })