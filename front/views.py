from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from time import sleep
from .models import Login
from .forms import UserForm, MessageForm
from .utils.weather import build_bot_response
from api.models import Person, Message
import requests


API_HOST = 'http://127.0.0.1:8000/api/'
options = {
    "weather": False
}


def index(request):
    if request.method == 'POST':
        tokens = requests.post(f'{API_HOST}token/', data={
            'username': request.POST['nickname'],
            'password': request.POST['password']
        })
        if tokens.status_code == 200:
            request.session['refresh_token'] = tokens.json()['refresh']
            request.session['access_token'] = tokens.json()['access']
            request.session['nickname'] = request.POST['nickname']
            return redirect('chat-page')
        else:
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
            user = request.session.get('nickname', 'Visitante')
            new_message_obj = {
                'content': form.cleaned_data['content'],
                'sender': user,
                'receiver': "Bot"
            }

            Message.objects.create(**new_message_obj)

            sleep(2)

            if "do tempo" in new_message_obj['content']:
                bot_response = "Perfeito! Agora me diga: qual cidade você gostaria de saber a previsão do tempo?"
                options["weather"] = True
            elif options["weather"]:
                bot_response = build_bot_response(new_message_obj['content'])
                options["weather"] = False
            else:
                bot_response = PHRASES.get(form.cleaned_data['content'].lower(), "I'm sorry, I don't understand that.")

            bot_message_obj = {
                'content': bot_response,
                'sender': "Bot",
                'receiver': user
            }

            Message.objects.create(**bot_message_obj)

    headers = {
        "Authorization": f"Bearer {request.session['access_token']}"
    }

    messages = requests.get(f'{API_HOST}messages/', headers=headers)
    context = {
        'messages': messages.json(),
        'form': form
    }
    return render(request, 'chat.html', context)
