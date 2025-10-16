from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import User
from django.contrib.auth.models import AnonymousUser


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            user = User.decode_jwt(token)
            if user:
                request.user = user
                return
        request.user = AnonymousUser()



