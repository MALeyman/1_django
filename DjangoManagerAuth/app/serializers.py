# app/serializers.py
from rest_framework import serializers
from .models import User, Role, Permission, UserRole

# Регистрация
class UserRegisterSerializer(serializers.ModelSerializer):
    '''  
    сериализатор для регистрации пользователя, 
    '''
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # По умолчанию роль User добавляется при создании
        from .models import Role, UserRole
        role_user = Role.objects.get(name='User')
        UserRole.objects.create(user=user, role=role_user)
        return user


# Авторизация
class UserLoginSerializer(serializers.Serializer):
    ''' 
    Сериализация авторизации
    '''
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# Сериализация получения данных профиля пользователя
class UserSerializer(serializers.ModelSerializer):
    ''' 
    Сериализация получения данных профиля пользователя
    '''
    # Получаем список ролей по связующей модели UserRole__role
    roles = serializers.SerializerMethodField()
    role_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all(),
        write_only=True,
        source='roles_rel'  
    )

    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'middle_name', 'email', 'is_active', 'is_superuser', 'roles', 'role_ids']

    def get_roles(self, obj):
        # Возвращаем роли пользователя — список ролей через связующую таблицу
        return RoleSerializer(Role.objects.filter(user_roles__user=obj), many=True).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret.get('roles'):
            # Если ролей нет, устанавливаем роль User по умолчанию
            from .models import Role
            user_role = Role.objects.filter(name='User').first()
            if user_role:
                ret['roles'] = [RoleSerializer(user_role).data]
        return ret


    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles_rel', None)  #
        instance = super().update(instance, validated_data)
        if roles_data is not None:
            # Удаляем старые связи UserRole
            UserRole.objects.filter(user=instance).delete()
            # Создаем новые
            for role in roles_data:
                UserRole.objects.create(user=instance, role=role)
        return instance











from rest_framework import serializers
from .models import RolePermission, Role, Permission


class RoleSerializer(serializers.ModelSerializer):
    ''' 
    Сериализация ролей
    '''
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class PermissionSerializer(serializers.ModelSerializer):
    ''' 
    Сериализация разрешений
    '''
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'description']


class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    permission_id = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), source='permission', write_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'role_id', 'permission_id']

    def create(self, validated_data):
        return RolePermission.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.permission = validated_data.get('permission', instance.permission)
        instance.save()
        return instance







