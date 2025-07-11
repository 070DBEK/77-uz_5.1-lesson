import django_filters
from .models import Ad


class AdFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_top = django_filters.BooleanFilter(field_name='is_top')
    seller_id = django_filters.NumberFilter(field_name='seller__id')
    district_id = django_filters.NumberFilter(method='filter_district_id')
    region_id = django_filters.NumberFilter(method='filter_region_id')
    category_ids = django_filters.CharFilter(method='filter_category_ids')

    class Meta:
        model = Ad
        fields = ['price__gte', 'price__lte', 'is_top', 'seller_id', 'district_id', 'region_id', 'category_ids']

    def filter_district_id(self, queryset, name, value):
        return queryset.filter(seller__addresses__district_id=value, seller__addresses__is_default=True)

    def filter_region_id(self, queryset, name, value):
        return queryset.filter(seller__addresses__region_id=value, seller__addresses__is_default=True)

    def filter_category_ids(self, queryset, name, value):
        if value:
            category_ids = [int(id.strip()) for id in value.split(',') if id.strip().isdigit()]
            return queryset.filter(category__id__in=category_ids)
        return queryset
