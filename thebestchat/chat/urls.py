from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('register', register, name='register'),
    path('auth', auth, name='auth'),
    path("logout/", LogoutView.as_view(next_page='auth'), name="logout"),

    path('invite', invite, name='invite'),

    path('', chat, name='chat'),
    path('<int:chat_id>', dialog, name='dialog')
]