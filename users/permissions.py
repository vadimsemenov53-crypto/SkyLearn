from rest_framework import permissions

class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    message = "Пользователь не является модератором."

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class IsCreator(permissions.BasePermission):
    """ Проверяет, является ли пользователь владельцем. """
    message = "Пользователь не является владельцем."

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            return True

        return False