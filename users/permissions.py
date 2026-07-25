from rest_framework import permissions

class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    message = 'Пользователь не является модератором'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()