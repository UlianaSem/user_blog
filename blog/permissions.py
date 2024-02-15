from rest_framework.permissions import BasePermission


class IsBlogOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.blog == request.user.blog

        return False
