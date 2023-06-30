from rest_framework import permissions

__all__ = [
    'IsWorkOwner',
]


class IsWorkOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.subject.user == request.user
