from rest_framework import permissions


class GetPermissionsReview(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class PostPermissionsReview(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff

