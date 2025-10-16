# управление ролями и правами

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Role, Permission, RolePermission
from ..serializers import RoleSerializer
from ..authentication import JWTAuthentication
from ..permissions import HasPermission, CanViewOrEditRoles
from rest_framework import status
from ..models import User, Role
from ..serializers import UserSerializer, RoleSerializer

# Управление ролями и правами (только для Admin)
class RolesListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = 'manage_roles'

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Роль создана'}, status=201)
        return Response(serializer.errors, status=400)


class RolePermissionsUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = 'manage_roles'

    def put(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=404)
        permission_ids = request.data.get('permission_ids', [])
        role.permissions.all().delete()
        for pid in permission_ids:
            try:
                perm = Permission.objects.get(id=pid)
                RolePermission.objects.create(role=role, permission=perm)
            except Permission.DoesNotExist:
                continue
        return Response({'message': 'Права роли обновлены'})




from rest_framework.permissions import AllowAny

class UsersWithRolesView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        roles = Role.objects.all()
        users_data = UserSerializer(users, many=True).data
        roles_data = RoleSerializer(roles, many=True).data
        return Response({'users': users_data, 'roles': roles_data})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Role, UserRole
from django.shortcuts import get_object_or_404



class UserRoleUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, HasPermission]  
    permission_classes = [AllowAny]
    # required_permission = 'manage_roles'
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        role_id = request.data.get('role_id')
        if not role_id:
            return Response({'detail': 'role_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        role = get_object_or_404(Role, pk=role_id)

        # Обновляем роль пользователя - удаляем все текущие и добавляем новую
        UserRole.objects.filter(user=user).delete()
        UserRole.objects.create(user=user, role=role)

        return Response({'detail': 'Role updated successfully'}, status=status.HTTP_200_OK)


class UserRoleAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, HasPermission]
    # permission_classes = [AllowAny]
    # permission_classes = [HasPermission]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CanViewOrEditRoles]


    def get(self, request):
        # Логика получения данных пользователей и ролей
        users = User.objects.all()
        roles = Role.objects.all()
        # print("ROLES", roles)
        users_data = UserSerializer(users, many=True).data
        roles_data = RoleSerializer(roles, many=True).data
        return Response({'users': users_data, 'roles': roles_data})

    def put(self, request, pk):
        def has_custom_perm(user, codename='moderate_content'):
            if user.is_superuser:
                # print("user.is_superuser", request.user.is_superuser)
                return True  # суперпользователь всегда имеет права
            
            for user_role in user.user_roles.all():
                role = user_role.role
                for role_perm in role.permissions.all():
                    if role_perm.permission.codename == codename:
                        return True
            return False

        # Логика обновления роли пользователя
        user = get_object_or_404(User, pk=pk)

        # Проверяем, что пользователь, роль которого хотим изменить, активен
        if not user.is_active:
            return Response({'detail': 'Пользователь не активен или не аутентифицирован'}, status=401)


        role_id = request.data.get('role_id')
        # print("request.user.roles", request.user.roles)
        # print("roles:", list(request.user.roles.all()))
        # print("role names:", [role.name for role in request.user.roles.all()])
        
        # user_roles = request.user.user_roles.all()
        # for user_role in user_roles:
        #     role = user_role.role
        #     permissions = role.permissions.all()  
        #     for role_perm in permissions:
        #         permission = role_perm.permission
        #         print(permission.codename, permission.description)

        
        if not has_custom_perm(request.user, 'moderate_content'):
            return Response({'detail': 'Нет прав на изменение'}, status=403)
        if not role_id:
            return Response({'detail': 'role_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        role = get_object_or_404(Role, pk=role_id)
        # Обновляем роль пользователя
        UserRole.objects.filter(user=user).delete()
        UserRole.objects.create(user=user, role=role)
        return Response({'detail': 'Role updated successfully'}, status=status.HTTP_200_OK)















