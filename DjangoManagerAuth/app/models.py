# app/models.py
from django.db import models
import bcrypt
import jwt                                 
from django.conf import settings
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, middle_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          middle_name=middle_name, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, middle_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, middle_name, password, **extra_fields)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)


class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(Role, through='UserRole', related_name='users')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def generate_jwt(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    @classmethod
    def decode_jwt(cls, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return cls.objects.get(id=payload['user_id'], is_active=True)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, cls.DoesNotExist):
            return None

    def soft_delete(self):
        self.is_active = False
        self.save()

    def update_profile(self, **kwargs):
        for field in ['first_name', 'last_name', 'middle_name', 'password']:
            if field in kwargs:
                if field == 'password':
                    self.set_password(kwargs[field])
                else:
                    setattr(self, field, kwargs[field])
        self.save()

    def __str__(self):
        return self.email



class Permission(models.Model):
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')










