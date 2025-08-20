from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class OwnershipMixin:
    """Ownership tekshirish uchun mixin"""

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'role'):
            if self.request.user.role in ['super_admin', 'admin']:
                return queryset
            elif hasattr(queryset.model, 'user'):
                return queryset.filter(user=self.request.user)
            elif hasattr(queryset.model, 'seller'):
                return queryset.filter(seller=self.request.user)
        return queryset


class SearchMixin:
    """Search functionality uchun mixin"""
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', '')

        if search_query and self.search_fields:
            search_q = Q()
            for field in self.search_fields:
                search_q |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(search_q)

        return queryset


class TimestampMixin:
    """Timestamp ma'lumotlari uchun mixin"""

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class BulkActionMixin:
    """Bulk actions uchun mixin"""

    def bulk_delete(self, request):
        """Bulk delete action"""
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(id__in=ids)
        count = queryset.count()
        queryset.delete()

        return Response({
            'message': f'{count} items deleted successfully'
        }, status=status.HTTP_200_OK)

    def bulk_update(self, request):
        """Bulk update action"""
        ids = request.data.get('ids', [])
        update_data = request.data.get('data', {})

        if not ids or not update_data:
            return Response({'error': 'IDs and data required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(id__in=ids)
        count = queryset.update(**update_data)

        return Response({
            'message': f'{count} items updated successfully'
        }, status=status.HTTP_200_OK)
