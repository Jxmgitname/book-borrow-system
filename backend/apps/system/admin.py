from django.contrib import admin

from system.models import Department, Menu, Role


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'leader', 'sort', 'status')
    search_fields = ('name', 'leader')
    list_filter = ('status',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'status', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('status',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'menu_type', 'parent', 'sort', 'status')
    search_fields = ('name', 'path', 'permission')
    list_filter = ('menu_type', 'status', 'visible')
