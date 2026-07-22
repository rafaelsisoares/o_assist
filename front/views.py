from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Login
from .forms import UserForm, LoginForm, MessageForm
from api.models import Person, Message


def index(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('nickname')
        password = data.get('password')

        try:
            user = User.objects.get(username=username, password=password)
            return redirect('home')
        except Login.DoesNotExist:
            return render(request, 'login.html', {'fail_login': True})
    return render(request, 'login.html', {'fail_login': False})


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            new_user = {
                "username": data['nickname'],
                "password": data['password'],
                "first_name": data['name'],
                "email": data['email'],
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
            }
            User.objects.create_user(**new_user)
            Person.objects.create(**data)
            return redirect('chat-page')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def chat(request):
    PHRASES = {
        "hello": "Hello! How can I assist you today?",
        "how are you?": "I'm just a bot, but I'm here to help you!",
        "what is your name?": "I am your friendly assistant bot.",
        "bye": "Goodbye! Have a great day!",
    }
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message_obj = {
                'content': form.cleaned_data['content'],
                'sender': request.user.username if request.user.is_authenticated else "Visitante",
                'receiver': "Bot"
            }

            Message.objects.create(**new_message_obj)

            bot_response = PHRASES.get(form.cleaned_data['content'].lower(), "I'm sorry, I don't understand that.")
            bot_message_obj = {
                'content': bot_response,
                'sender': "Bot",
                'receiver': request.user.username if request.user.is_authenticated else "Visitante"
            }

            Message.objects.create(**bot_message_obj)

    messages = Message.objects.all()
    context = {
        'messages': messages,
        'form': form
    }
    return render(request, 'chat.html', context)
