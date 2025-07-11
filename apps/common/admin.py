from django.contrib import admin
from .models import Region, District, StaticPage, Setting


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'created_at']
    list_filter = ['region', 'created_at']
    search_fields = ['name', 'region__name']


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['phone', 'support_email', 'app_version', 'maintenance_mode']

    def has_add_permission(self, request):
        return not Setting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
