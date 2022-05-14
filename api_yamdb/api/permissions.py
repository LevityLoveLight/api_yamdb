from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
        )


class ReviewAndCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or (request.user
                    and request.user.is_authenticated
                    )
                )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return (request.user
                    and request.user.is_authenticated)
        if request.method == 'PATCH' or request.method == 'DELETE':
            return (request.user.role == 'admin'
                    or request.user.role == 'moderator'
                    or obj.author == request.user)
        return False
