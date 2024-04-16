from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend

from fav_link.filtersets import FavoriteUrlFilter
from fav_link.models import FavoriteUrl, Tag, Category
from fav_link.serializers import (
    FavoriteUrlSerializer,
    CategorySerializer,
    TagSerializer,
)


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
    permission_classes = [ObjectOwnerPermission]

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
    permission_classes = [ObjectOwnerPermission]

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
    filterset_class = FavoriteUrlFilter

    def get_queryset(self):
        return super().get_queryset()

    def filter_queryset(self, queryset):
        if hasattr(self.request, "user"):
            queryset = queryset.filter(owner=self.request.user)
        return super().filter_queryset(queryset)

    def update(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        partial = kwargs.pop("partial", False)

        # select for update instance
        with transaction.atomic():
            instance = FavoriteUrl.objects.select_for_update().filter(id=pk).last()

            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)

            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
