from datetime import timedelta
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import User, Session, Article, AccessRule
from uuid import uuid4
import bcrypt


@csrf_exempt
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


@csrf_exempt
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


def logout(request):
    user = request.user
    if isinstance(user, User):
        Session.objects.filter(user=user).delete()
        response = HttpResponse('Вы вышли из аккаунта')
        response.delete_cookie('sessionid')

    else:
        response = HttpResponse('Вы не вышли из аккаунта')

    return response


def delete_account(request):
    user = request.user
    if isinstance(user, User):
        Session.objects.filter(user=user).delete()
        user.is_active = False
        user.save()
        response = HttpResponse('Вы удалили аккаунт')
        response.delete_cookie('sessionid')

    else:
        response = HttpResponse('Аккаунт не был удален')

    return response


@csrf_exempt
def update_profile(request):
    user = request.user
    if isinstance(user, User) and request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        if name:
            user.name = name
        if surname:
            user.surname = surname

        user.save()
        return HttpResponse('Данные аккаунта успешно обновлены')

    return HttpResponse('Данные аккаунта не обновлены')


def delete_article(request, article_id):
    user = request.user
    if not isinstance(user, User):
        return HttpResponseForbidden('Пользователь не авторизирован')

    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return HttpResponseNotFound('Статья не найдена')

    rule = AccessRule.objects.filter(role=user.role, element_name='Article').first()
    if rule is None:
        return HttpResponseForbidden('Нет прав доступа')

    if rule.delete_all_permission or (rule.delete_own_permission and article.owner == user):
        article.delete()
        return HttpResponse('Статья удалена')

    return HttpResponseForbidden('Нет прав доступа для этого действия')