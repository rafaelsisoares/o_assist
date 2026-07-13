from django.shortcuts import render, redirect
from .models import Login, User


def index(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        data = request.POST

        if data.is_valid():
            User.objects.create(**data.cleaned_data)
            return redirect('login')

    return render(request, 'register.html')
