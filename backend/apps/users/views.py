from django.contrib.auth import authenticate
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from backend.response import error_response, success_response
from users.models import User
from users.serializers import (
    RegisterSerializer,
    UserCreateUpdateSerializer,
    UserSerializer,
)

#登录视图
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return error_response('账号或密码不正确', code=400, status_code=400)
        if not user.status:
            return error_response('账号已停用', code=400, status_code=400)

        token = str(RefreshToken.for_user(user).access_token)
        avatar = user.avatar or '/favicon.ico'
        return success_response({
            'token': token,
            'name': user.nickname or user.username,
            'avatar': avatar,
        }, message='登录成功')

#用户信息视图
class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        avatar = user.avatar or '/favicon.ico'
        return success_response({
            'name': user.nickname or user.username,
            'avatar': avatar,
        })

#注册视图
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success_response(UserSerializer(user).data, message='注册成功', status_code=status.HTTP_201_CREATED)

#用户视图
class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UserCreateUpdateSerializer
        return UserSerializer
