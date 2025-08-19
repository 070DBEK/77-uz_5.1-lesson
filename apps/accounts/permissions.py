from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsSuperAdmin(permissions.BasePermission):
    """
    Super Admin - barcha huquqlar
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role == 'super_admin'
        )


class IsAdmin(permissions.BasePermission):
    """
    Admin - sotuvchilarni boshqarish
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin']
        )


class IsSeller(permissions.BasePermission):
    """
    Seller - faqat o'z mahsulotlari
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin', 'seller']
        )


class CanApplyForSeller(permissions.BasePermission):
    """
    Customer'lar seller bo'lish uchun ariza bera oladi
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role == 'customer'  # Faqat customer'lar ariza bera oladi
        )


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Seller - o'qish uchun hamma, yozish uchun faqat seller
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
    Faqat owner yoki admin
    """

    def has_object_permission(self, request, view, obj):
        # Super admin va admin hamma narsaga ruxsat
        if request.user.role in ['super_admin', 'admin']:
            return True

        # Owner o'z obyektlariga ruxsat
        if hasattr(obj, 'seller'):
            return obj.seller == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user

        return False


class CanManageSellers(permissions.BasePermission):
    """
    Sotuvchilarni boshqarish uchun
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['super_admin', 'admin']
        )
