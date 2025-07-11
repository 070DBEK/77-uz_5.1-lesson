from django.contrib import admin
from .models import Category, Ad, AdPhoto, FavouriteProduct, MySearch, PopularSearchTerm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name']
    list_editable = ['is_active']


class AdPhotoInline(admin.TabularInline):
    model = AdPhoto
    extra = 1


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'price', 'status', 'is_top', 'view_count', 'published_at']
    list_filter = ['status', 'is_top', 'category', 'published_at']
    search_fields = ['name_uz', 'name_ru', 'seller__full_name']
    list_editable = ['status', 'is_top']
    readonly_fields = ['slug', 'view_count', 'published_at']
    inlines = [AdPhotoInline]

    actions = ['approve_ads', 'reject_ads', 'make_top']

    def approve_ads(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f'{queryset.count()} ads approved.')

    def reject_ads(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} ads rejected.')

    def make_top(self, request, queryset):
        queryset.update(is_top=True)
        self.message_user(request, f'{queryset.count()} ads marked as top.')

    approve_ads.short_description = 'Approve selected ads'
    reject_ads.short_description = 'Reject selected ads'
    make_top.short_description = 'Mark as top ads'


@admin.register(AdPhoto)
class AdPhotoAdmin(admin.ModelAdmin):
    list_display = ['ad', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']


@admin.register(FavouriteProduct)
class FavouriteProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'device_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__phone_number', 'product__name_uz', 'device_id']


@admin.register(MySearch)
class MySearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'search_query', 'price_min', 'price_max', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['user__phone_number', 'search_query']


@admin.register(PopularSearchTerm)
class PopularSearchTermAdmin(admin.ModelAdmin):
    list_display = ['name', 'search_count', 'category', 'updated_at']
    list_filter = ['category', 'updated_at']
    search_fields = ['name']
    readonly_fields = ['search_count']
