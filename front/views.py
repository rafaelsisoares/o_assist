from django.shortcuts import render, redirect
from .models import Login, User, Message
from .forms import UserForm, LoginForm


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
    messages = Message.objects.all()
    context = {
        'messages': messages,
    }
    return render(request, 'chat.html', context)
