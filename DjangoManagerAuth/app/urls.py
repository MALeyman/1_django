# app/urls.py
from django.urls import path
from .views import RegisterView, LoginView, ProfileView, RolesListView, RolePermissionsUpdateView, UsersWithRolesView, UserRoleAPIView, RolePermissionAPIView
from .views import HomeView  
from .views import DocumentMockView, CheckPermissionView
from .views import RegisterView, LoginView
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRoleUpdateAPIView
import os


urlpatterns = [
    path('', HomeView.as_view(), name='home'),                                      #  главная страница
    path('register/', RegisterView.as_view()),                                      # Регистрация
    path('login/', LoginView.as_view()),                                            # Авторизация
    path('profile/', ProfileView.as_view()),                                        # Профиль пользователя
    path('api/profile/delete/', ProfileView.as_view(), name='user-soft-delete'),    # Удаление профиля
    path('api/users/roles/', UserRoleAPIView.as_view()),                            # Роли пользователей
    path('api/users/<int:pk>/role/', UserRoleAPIView.as_view()),                    # Отправка изменений роли пользователя на сервер  
    # path('api/users-with-roles/<int:pk>/', UserRoleAPIView.as_view()),
    path('api/role-permissions/', RolePermissionAPIView.as_view(), name='role-permissions'),                  # Правила для роли
    path('api/role-permissions/<int:pk>/', RolePermissionAPIView.as_view(), name='role-permissions-detail'),  # Отправка изменений правил на сервер
    path('api/check-permission/', CheckPermissionView.as_view(), name='mock-documents'),                       # Документы
    path('mock/documents/', DocumentMockView.as_view(), name='mock-documents'),




    # path('admin/roles/', RolesListView.as_view()),
    # path('admin/roles/<int:role_id>/permissions/', RolePermissionsUpdateView.as_view()),
    # path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'app/images/favicon.ico')),
    # path('api/roles/<int:role_id>/permissions/', RolePermissionsUpdateView.as_view(), name='role-permissions-update'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('api/roles/', RolesListView.as_view(), name='roles-list'),
    # path('users/<int:pk>/role/', UserRoleUpdateAPIView.as_view(), name='user-role-update'),

    

    
 

]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# для разработки 
if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'app', 'static'))

