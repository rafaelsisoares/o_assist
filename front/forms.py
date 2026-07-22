from django import forms
from .models import Login
from api.models import Person, Message


class UserForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'nickname', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'name': 'Nome',
            'nickname': 'Nome de usuário',
            'email': 'E-mail',
            'password': 'Senha',
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
