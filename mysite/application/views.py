from django.http import HttpResponse
from django.shortcuts import render
from .models import User
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