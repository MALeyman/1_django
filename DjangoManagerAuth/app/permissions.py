# app/permissions.py
from rest_framework import permissions
from .models import UserRole, RolePermission, Permission
from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)

class HasPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        logger.debug("HasPermission.has_permission called")
        user_roles = request.user.user_roles.all()
        logger.debug(f"User roles: {[ur.role.name for ur in user_roles]}")
        if user_roles.filter(role__name='Admin').exists():
            logger.debug("Access granted: Admin role found")
            return True

        logger.debug("Access denied")
        return False



class CanViewOrEditRoles(permissions.BasePermission):
    """
    Просмотр ролей — для Admin и Moderator.
    Редактирование — только если в ролях пользователя есть permission с codename 'moderate_content'.
    """

    message = 'Нет прав на изменение ролей'

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Получаем роли пользователя
        user_roles = user.user_roles.all()  
        # print("user.is_superuser 1", user.is_superuser)
        role_names = [ur.role.name for ur in user_roles]
        # Разрешаем просмотр (GET, HEAD, OPTIONS) для Admin и Moderator
        # print("permissions.SAFE_METHODS", permissions.SAFE_METHODS)
        # print("request.method ", request.method )
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            # print("user.is_superuser 2", user.is_superuser)
            if 'Admin' in role_names or 'Moderator' in role_names or user.is_superuser:
                return True
            return False
        
        # Для модифицирующих запросов (POST, PUT, PATCH, DELETE)
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            # Получаем все permissions, которые есть у ролей пользователя
            # print("user.is_superuser 3", user.is_superuser)
            perms_codenames = set(
                Permission.objects.filter(
                    role_permissions__role__in=[ur.role for ur in user_roles]
                ).values_list('codename', flat=True)
            )
            if user.is_superuser:
                return True

            # Разрешаем, если у пользователя есть perm 'moderate_content'
            return 'moderate_content' in perms_codenames

        return False





class FullAdminAccessPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
                return True
        # Проверяем наличие права 'full_admin_access'
        user_roles = user.user_roles.all()

        perm_codenames = set(
            Permission.objects.filter(
                role_permissions__role__in=[ur.role for ur in user_roles]
            ).values_list('codename', flat=True)
        )
        return 'full_admin_access' in perm_codenames







