from django.urls import include, path
from rest_framework.routers import DefaultRouter

from system.views import DepartmentViewSet, MenuViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
   
]

urlpatterns += router.urls
