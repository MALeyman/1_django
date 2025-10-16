# app/authentication.py
from rest_framework import authentication, exceptions
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        user = User.decode_jwt(token)
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid or expired token')
        return (user, token)

