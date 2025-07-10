from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address, SellerRegistration


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone_number', 'full_name', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'created_at']
    search_fields = ['phone_number', 'full_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('full_name', 'profile_photo')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at']
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
