from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm, MessageForm
from .utils.weather import build_bot_response
from .utils.current_time import current_time
from api.models import Person, Message
from AI.views import generate_text
import requests
import os


API_HOST = os.environ.get('API_HOST', 'http://127.0.0.1:8000/api/')
options = {
    "weather": False
}


def index(request):
    if request.method == 'POST':
        tokens = requests.post(f'{API_HOST}token/', data={
            'username': request.POST['nickname'],
            'password': request.POST['password']
        }, timeout=5)
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
            response_tokens = requests.post(f'{API_HOST}token/', data={
                'username': data['nickname'],
                'password': data['password']
            }, timeout=5)
            if response_tokens.status_code == 200:
                request.session['refresh_token'] = response_tokens.json()['refresh']
                request.session['access_token'] = response_tokens.json()['access']
                request.session['nickname'] = data['nickname']
            Person.objects.create(**data)
            return redirect('chat-page')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def chat(request):
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

            match new_message_obj['content'].lower():
                case content if "horas" in content:
                    bot_response = f"Agora são {current_time()}"
                case content if "do tempo" in content:
                    bot_response = "Perfeito! Agora me diga: qual cidade você gostaria de saber a previsão do tempo?"
                    options["weather"] = True
                case content if options["weather"]:
                    bot_response = build_bot_response(new_message_obj['content'])
                    options["weather"] = False
                case _:
                    bot_response = generate_text(new_message_obj['content'])

            bot_message_obj = {
                'content': bot_response,
                'sender': "Bot",
                'receiver': user
            }

            Message.objects.create(**bot_message_obj)

    headers = {
        "Authorization": f"Bearer {request.session['access_token']}"
    }

    response_messages = requests.get(f'{API_HOST}messages/', headers=headers)
    if response_messages.status_code == 401:
        refresh_token = request.session.get('refresh_token')
        refresh_response = requests.post(f'{API_HOST}token/refresh/', data={'refresh': refresh_token})
        if refresh_response.status_code == 200:
            request.session['access_token'] = refresh_response.json()['access']
            headers["Authorization"] = f"Bearer {request.session['access_token']}"
            response_messages = requests.get(
                f'{API_HOST}messages/', headers=headers
                )
        else:
            return redirect('login-page')
    context = {
        'messages': response_messages.json(),
        'form': form
    }
    return render(request, 'chat.html', context)
