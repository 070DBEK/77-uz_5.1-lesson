from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsSuperAdmin(permissions.BasePermission):
    """
    Super Admin - all rights
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role == 'super_admin'
        )


class IsAdmin(permissions.BasePermission):
    """
    Admin - manage sellers
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin']
        )


class IsSeller(permissions.BasePermission):
    """
    Seller - only own products
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin', 'seller']
        )


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Seller - everyone can read, only seller can write
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin', 'seller']
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Only owner or admin
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['super_admin', 'admin']:
            return True
        if hasattr(obj, 'seller'):
            return obj.seller == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user

        return False


class CanManageSellers(permissions.BasePermission):
    """
    To manage sellers
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin']
        )

