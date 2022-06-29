from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Доступ только для администратора остальным только чтение."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение внесение изменений автору и админу, остальные чтение."""
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user == obj.author
            )
        ) or request.method in permissions.SAFE_METHODS


class IsOwnerAdmin(permissions.BasePermission):
    """Разрешено вносить изменения владельцу и админу"""
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user and request.user.is_admin
        )
