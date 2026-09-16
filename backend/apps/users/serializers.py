from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from system.models import Role
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    role_names = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nickname', 'email', 'phone', 'avatar',
            'status', 'is_staff', 'is_superuser', 'department', 'department_name',
            'roles', 'role_names', 'last_login', 'date_joined', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'last_login', 'date_joined', 'created_at', 'updated_at')

    def get_role_names(self, obj):
        return list(obj.roles.values_list('name', flat=True))


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all(),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'nickname', 'email', 'phone',
            'avatar', 'status', 'is_staff', 'department', 'roles',
        )

    def validate_phone(self, value):
        return value or None

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password('123456')
        user.save()
        if roles:
            user.roles.set(roles)
        return user

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if roles is not None:
            instance.roles.set(roles)
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'nickname', 'email', 'phone')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value

    def validate_phone(self, value):
        return value or None

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次输入的密码不一致'})
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        if not user.nickname:
            user.nickname = user.username
        user.set_password(password)
        user.save()
        return user
