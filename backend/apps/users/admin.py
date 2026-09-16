from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nickname', 'email', 'phone', 'status', 'is_staff', 'date_joined')
    search_fields = ('username', 'nickname', 'email', 'phone')
    list_filter = ('status', 'is_staff', 'is_superuser')
