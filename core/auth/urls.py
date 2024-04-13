from core.auth.views import (
    UserViewSet,
    LoginViewSet,
    LogoutViewSet,
    UserRegistrationViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("login", LoginViewSet, basename="login")
router.register("logout", LogoutViewSet, basename="logout")
router.register("user", UserViewSet, basename="user")

router.register("registration", UserRegistrationViewSet, basename="registration")
