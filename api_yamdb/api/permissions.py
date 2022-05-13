from rest_framework import permissions


class ReviewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        if request.method == 'GET':
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
