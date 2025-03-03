from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission: Only admin users can access this view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Only allow admin users


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission: Allow users to access their own tasks, but admin can access all tasks.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user  # Admins or task owners only
