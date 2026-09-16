from rest_framework import serializers

from system.models import Department, Menu, Role


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    menu_ids = serializers.PrimaryKeyRelatedField(
        source='menus',
        many=True,
        queryset=Menu.objects.all(),
        required=False,
    )

    class Meta:
        model = Role
        fields = ('id', 'name', 'code', 'description', 'status', 'menu_ids', 'created_at', 'updated_at')
