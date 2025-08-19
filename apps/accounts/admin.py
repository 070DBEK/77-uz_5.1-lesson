from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address, SellerRegistration


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone_number', 'full_name', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'created_at']
    search_fields = ['phone_number', 'full_name']
    ordering = ['-created_at']
    readonly_fields = ['last_login', 'date_joined', 'created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('full_name', 'profile_photo')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'password1', 'password2', 'role'),
        }),
    )

    # Admin actions qo'shish
    actions = ['make_verified', 'make_unverified', 'make_seller', 'make_customer']

    def make_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f'{queryset.count()} users marked as verified.')

    def make_unverified(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f'{queryset.count()} users marked as unverified.')

    def make_seller(self, request, queryset):
        queryset.update(role='seller', is_verified=True)
        self.message_user(request, f'{queryset.count()} users changed to seller.')

    def make_customer(self, request, queryset):
        queryset.update(role='customer', is_verified=False)
        self.message_user(request, f'{queryset.count()} users changed to customer.')

    make_verified.short_description = 'Mark selected users as verified'
    make_unverified.short_description = 'Mark selected users as unverified'
    make_seller.short_description = 'Change selected users to seller'
    make_customer.short_description = 'Change selected users to customer'

    def has_change_permission(self, request, obj=None):
        if obj and obj.role == 'super_admin' and request.user.role != 'super_admin':
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.role == 'super_admin' and request.user.role != 'super_admin':
            return False
        return super().has_delete_permission(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'admin':
            return qs.exclude(role='super_admin')
        return qs


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'region', 'district', 'is_default', 'created_at']
    list_filter = ['is_default', 'region', 'created_at']
    search_fields = ['user__phone_number', 'name']


@admin.register(SellerRegistration)
class SellerRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'project_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'project_name', 'phone_number']
    actions = ['approve_registrations', 'reject_registrations']

    def approve_registrations(self, request, queryset):
        for registration in queryset:
            registration.status = 'approved'
            registration.save()
            # Update user role to seller
            registration.user.role = 'seller'
            registration.user.save()
        self.message_user(request, f'{queryset.count()} registrations approved.')

    def reject_registrations(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} registrations rejected.')

    approve_registrations.short_description = 'Approve selected registrations'
    reject_registrations.short_description = 'Reject selected registrations'

    def has_change_permission(self, request, obj=None):
        return request.user.role in ['super_admin', 'admin']

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['super_admin', 'admin']
