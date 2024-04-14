from account.views import (
    UserViewSet,
    LoginViewSet,
    LogoutViewSet,
    UserRegistrationViewSet,
    UserChangePasswordViewSet,
)

from rest_framework import routers
from django.urls import include, path

router = routers.DefaultRouter()
router.register("login", LoginViewSet, basename="login")
router.register("logout", LogoutViewSet, basename="logout")
router.register("user-info", UserViewSet, basename="user-info")
router.register("registration", UserRegistrationViewSet, basename="registration")
router.register(
    "change-password", UserChangePasswordViewSet, basename="change-password"
)

urlpatterns = router.urls
