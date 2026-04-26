from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import User, Session
from uuid import uuid4
import bcrypt


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        if User.objects.filter(email=email).exists():
            return HttpResponse('Пользователь с таким email уже существует')

        if password != repeat_password:
            return HttpResponse('Пароли различаются')

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_password_decoded = hashed_password.decode('utf-8')

        User.objects.create(name=name, surname=surname,
                            patronymic=patronymic, email=email,
                            password=hashed_password_decoded)

        return HttpResponse('Регистрация прошла успешно!')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                random_key = str(uuid4())
                expire_time = timezone.now() + timedelta(days=7)
                Session.objects.update_or_create(user=user, defaults={'session': random_key, 'expire_at': expire_time})
                response = HttpResponse('Авторизация успешно выполнена!')
                response.set_cookie(key='sessionid', value=random_key, expires=expire_time)
                return response

            return HttpResponse('Пароль неверный')

        return HttpResponse('Такого пользователя нет')
