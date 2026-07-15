from django.urls import path
from .views import index, register

urlpatterns = [
    path('', index, name='login-page'),
    path('register/', register, name='register-page'),
]
