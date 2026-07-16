from django.urls import path
from .views import index, register, chat

urlpatterns = [
    path('', index, name='login-page'),
    path('register/', register, name='register-page'),
    path('chat/', chat, name='chat-page'),
]
