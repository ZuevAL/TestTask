from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)