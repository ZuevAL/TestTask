from .models import User, Session
from django.utils import timezone


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cookie = request.COOKIES.get('sessionid')
        session_obj = Session.objects.filter(session=cookie).first()
        if session_obj and timezone.now() < session_obj.expire_at:
            request.user = session_obj.user

        response = self.get_response(request)
        return response