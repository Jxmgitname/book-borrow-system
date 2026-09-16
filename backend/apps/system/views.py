from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from backend.response import error_response, success_response
from system.models import Department, Menu, Role
from system.serializers import DepartmentSerializer, MenuSerializer, RoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().prefetch_related('menus')
    serializer_class = RoleSerializer



class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
