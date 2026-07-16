from django.shortcuts import render, redirect
from .models import Login, User, Message
from .forms import UserForm, LoginForm, MessageForm


def index(request):
    if request.method == 'POST' and "username" in request.POST:
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        try:
            login = Login.objects.get(username=username, password=password)
            user = User.objects.get(user=login.username)
            return redirect('home')
        except Login.DoesNotExist:
            return render(request, 'login.html', {'fail_login': True})
    return render(request, 'login.html', {'fail_login': False})


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            User.objects.create(**form.cleaned_data)
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
