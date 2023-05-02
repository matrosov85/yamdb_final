from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or (
                    request.user.is_authenticated
                    and request.user.role == 'admin'
        ))


class IsAdminAuthorOrReadOnly:

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or object.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
