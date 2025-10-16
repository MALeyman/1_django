# регистрация, вход, выход

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserRegisterSerializer
from ..models import User
from django.views import View
from django.http import JsonResponse
from ..serializers import UserLoginSerializer

import json
from django.utils import timezone


#  Регистрация
class RegisterView(View):
    ''' 
    Регистрация пользователя
    '''
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Пользователь успешно зарегистрирован'})
            return JsonResponse(serializer.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный формат данных'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# class RegisterView(View):
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             email = data['email']
#             first_name = data['first_name']
#             last_name = data['last_name']
#             middle_name = data.get('middle_name', '')
#             password = data['password']
#             password_confirm = data['password_confirm']

#             if password != password_confirm:
#                 return JsonResponse({'error': 'Пароли не совпадают'}, status=400)

#             if User.objects.filter(email=email).exists():
#                 return JsonResponse({'error': 'Пользователь с таким email уже существует'}, status=400)

#             user = User(
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#                 middle_name=middle_name,
#                 is_active=True,
#             )
#             user.set_password(password)
#             user.save()

#             return JsonResponse({'message': 'Пользователь успешно зарегистрирован'})
#         except KeyError:
#             return JsonResponse({'error': 'Некорректные данные'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)



#  Авторизация
class LoginView(View):
    ''' 
    Авторизация пользователя
    '''
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']

                user = User.objects.filter(email=email, is_active=True).first()
                if not user or not user.check_password(password):
                    return JsonResponse({'error': 'Неверный email или пароль'}, status=401)

                token = user.generate_jwt()

                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])

                return JsonResponse({'token': token})
            else:
                return JsonResponse(serializer.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректные данные'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



