from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.TextField()
    sender = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
