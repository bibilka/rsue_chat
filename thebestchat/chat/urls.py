from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('user/<int:id>/', user),

    path('register', register, name='register'),
    path('auth', auth, name='auth'),
    path("logout/", LogoutView.as_view(next_page='auth'), name="logout"),

    path('', chat, name='chat')
]