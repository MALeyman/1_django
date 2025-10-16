# профиль пользователя

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers import UserSerializer
from ..authentication import JWTAuthentication
from rest_framework import status
from ..permissions import HasPermission



# Профиль пользователя (просмотр, обновление, удаление)
class ProfileView(APIView):
    ''' 
    Профиль пользователя 
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Данные обновлены'})
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = request.user
        if user.is_superuser:
            return Response({'detail': 'Нельзя удалить суперпользователя'}, status=403)
        user.is_active = False
        user.save()
        return Response({'message': 'Аккаунт деактивирован'})







# class UserSoftDeleteAPI(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated, HasPermission]
#     required_permission = 'delete_user'
#     def put(self, request):
#         user = request.user
#         user.is_active = False
#         user.save()
#         return Response({'detail': 'Профиль успешно удалён'}, status=status.HTTP_200_OK)


