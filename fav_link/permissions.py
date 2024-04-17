from rest_framework.permissions import IsAuthenticated


class ObjectOwnerPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            return obj.owner == request.user

        return False
