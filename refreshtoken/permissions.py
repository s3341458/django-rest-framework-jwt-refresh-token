from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Only admins or owners are allowed.
    """
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow staff or superusers, and the owner of the object itself.
        """
        user = request.user
        if not user.is_authenticated:
            return False
        elif user.is_staff or user.is_superuser:
            return True
        return user == obj.user
