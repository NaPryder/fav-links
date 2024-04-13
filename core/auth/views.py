from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from core.auth.serializers import (
    UserSerializer,
    SessionLoginSerializer,
    UserRegistrationSerializer,
)

from rest_framework import viewsets, serializers, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.decorators import action

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters


class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    serializer_class = UserSerializer

    @action(["POST"], detail=True, permission_classes=[DjangoModelPermissions])
    def reset_password(self, request, pk):
        pass


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = SessionLoginSerializer
    permission_classes = []

    # @method_decorator(never_cache)
    # @method_decorator(csrf_protect)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
        except Exception as e:
            try:
                assert isinstance(e, serializers.ValidationError)
                return Response(e.detail["non_field_errors"][0], 400)
            except:
                return Response("Unable to log in with provided credentials.", 400)

        login(request, user)
        return Response(serializer.data)

    def get_view_name(self):
        return "Login"


class LogoutViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.Serializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logout(request)
        return Response({})

    def get_view_name(self):
        return "Logout"
