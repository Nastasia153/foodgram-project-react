from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Allows access only to administrators or read only."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Object level permission that allows access for writing to
    staff or object author
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user == obj.author
            )
        ) or request.method in permissions.SAFE_METHODS
