from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    message = "Пользователь не является модератором."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsCreator(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            return True

        return False


class IsProfile(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем профиля."""

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True

        return False
