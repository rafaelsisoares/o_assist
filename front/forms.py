from django import forms
from .models import User, Login


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'user', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'name': 'Nome',
            'user': 'Nome de usuário',
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
