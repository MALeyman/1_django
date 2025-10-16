from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models import UserRole, RolePermission, Permission
from ..authentication import JWTAuthentication
from ..serializers import RolePermissionSerializer
from ..permissions import FullAdminAccessPermission
from django.shortcuts import get_object_or_404



class RolePermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, FullAdminAccessPermission]

    def get(self, request):
        role_permissions = RolePermission.objects.all()
        
        serializer = RolePermissionSerializer(role_permissions, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        role_permission = get_object_or_404(RolePermission, pk=pk)
        serializer = RolePermissionSerializer(role_permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
