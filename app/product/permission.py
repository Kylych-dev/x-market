from rest_framework import permissions

class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Разрешить все без ограничений для безопасных (GET, HEAD, OPTIONS) методов
        return request.user.is_authenticated  # Проверить, аутентифицирован ли пользователь для не безопасных методов (POST, PUT, DELETE)
