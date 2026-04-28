from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=50)


class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission)


class User(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)


class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session = models.CharField(max_length=255)
    expire_at = models.DateTimeField()