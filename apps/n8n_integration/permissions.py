from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Only allow owners to edit their own objects
        return obj.owner == request.user

class IsAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated