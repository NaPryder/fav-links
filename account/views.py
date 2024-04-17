from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from account.serializers import (
    UserInfoSerializer,
    SessionLoginSerializer,
    UserRegistrationSerializer,
)

from rest_framework import viewsets, serializers, mixins
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    DjangoObjectPermissions,
)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from account.permissions import UserOwnerInfoPermission
from rest_framework import status


class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [DjangoObjectPermissions, UserOwnerInfoPermission]

    lookup_field = "username"
    lookup_value_regex = "[^/]+"

    @method_decorator(ensure_csrf_cookie)
    def list(self, request, *args, **kwargs):
        if (user := request.user).is_authenticated:
            return Response(self.get_serializer(user).data)
        else:
            return Response("Fail", status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = SessionLoginSerializer
    permission_classes = [AllowAny]

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
        except Exception as e:
            return Response("Unable to log in with provided credentials.", 400)

        login(request, user)
        return Response(UserInfoSerializer(user, context={"request": request}).data)

    def get_view_name(self):
        return "Login"


class LogoutViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.Serializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logout(request)
        return Response(dict(status="success"))

    def get_view_name(self):
        return "Logout"
