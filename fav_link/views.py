from django.http import QueryDict
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.validators import ValidationError

from rest_framework.permissions import IsAuthenticated, BasePermission
from fav_link.models import FavoriteUrl, Tag, Category
from fav_link.serializers import (
    FavoriteUrlSerializer,
    CategorySerializer,
    TagSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend


class ObjectOwnerPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            return obj.owner == request.user

        return False


class ManageTagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "name"
    pagination_class = None

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @action(["GET"], detail=False)
    def add_sample(self, request):
        data = {"name": "sample-1", "owner": request.user.id}
        serializer = TagSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(dict(success=True, **serializer.data))


class ManageCategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class FavoriteUrlViewSet(ModelViewSet):
    queryset = (
        FavoriteUrl.objects.prefetch_related("tags").select_related("category").all()
    )
    serializer_class = FavoriteUrlSerializer

    permission_classes = [ObjectOwnerPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "tags", "create_at"]

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)

    #     successful_message = dict(message="success", **serializer.data)
    #     print("---successfull", successful_message)
    #     return Response(
    #         successful_message, status=status.HTTP_201_CREATED, headers=headers
    #     )
