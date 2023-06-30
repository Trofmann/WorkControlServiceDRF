from rest_framework import permissions

__all__ = [
    'IsSubjectOwner',
]


class IsSubjectOwner(permissions.IsAuthenticated):
    """Allows access only authenticated owner"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
