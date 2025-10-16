 # бизнес-ресурсы (Mock API)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..authentication import JWTAuthentication
from ..permissions import HasPermission
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

# Пример "ресурса" - фиктивные документы
DOCUMENTS = [
    {'id': 1, 'user_id': 1, 'title': 'Документ 1', 'content': 'Содержание первого документа'},
    {'id': 2, 'user_id': 2, 'title': 'Документ 2', 'content': 'Содержание второго документа'},
]

@method_decorator(csrf_exempt, name='dispatch')
class DocumentMockView(View):
    def get(self, request):
   

        return JsonResponse({'documents': DOCUMENTS})



class CheckPermissionView(APIView):
    authentication_classes = [JWTAuthentication]
 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        def has_custom_perm(user, codename='view_documents'):

            # for user_role in user.user_roles.all():
            #     role = user_role.role
            #     print("user_role 11", role.permissions.all())
            #     for role_perm in role.permissions.all():
            #         print("role_perm 12", role_perm.permission.codename)
            #         if role_perm.permission.codename == codename:
            #             print("codename 22", codename)



            for user_role in user.user_roles.all():
                role = user_role.role
                for role_perm in role.permissions.all():
                    if role_perm.permission.codename == codename:
                        return True
            return False

        user = request.user
        has_permission = False

        if user.is_superuser:
            return Response({'has_permission': True}, status=status.HTTP_200_OK)
        if not has_custom_perm(request.user, 'view_documents'):
            return Response({'detail': 'Доступ запрещён'}, status=403)
        return Response({'has_permission': True}, status=status.HTTP_200_OK)









        # if user.is_superuser:
        #     has_permission = True
        # else:

        #     has_permission = has_custom_perm(request.user,'view_documents')
        # return Response({'has_permission': has_permission})


