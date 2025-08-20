from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsSuperAdmin(permissions.BasePermission):
    """Super Admin permission"""

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role == 'super_admin'
        )


class IsAdmin(permissions.BasePermission):
    """Admin permission"""

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin']
        )


class IsSeller(permissions.BasePermission):
    """Seller permission"""

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin', 'seller']
        )


class CanApplyForSeller(permissions.BasePermission):
    """Customer can apply for seller"""

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role == 'customer'
        )


class IsSellerOrReadOnly(permissions.BasePermission):
    """Read for all, write for sellers only"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin', 'seller']
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Owner or admin only"""

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['super_admin', 'admin']:
            return True

        if hasattr(obj, 'seller'):
            return obj.seller == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user

        return False


class CanManageSellers(permissions.BasePermission):
    """Can manage sellers"""

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin']
        )
