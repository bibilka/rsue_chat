from django.urls import path
from .views import *

urlpatterns = [
    path('user/<int:id>/', user),
    path('register', register, name='register'),
    path('', chat, name='room')
]