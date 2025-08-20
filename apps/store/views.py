from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .models import Category, Ad, AdPhoto, FavouriteProduct, MySearch, PopularSearchTerm
from .serializers import *
from .filters import AdFilter
from apps.accounts.permissions import IsSeller, IsOwnerOrAdmin, IsSellerOrReadOnly


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True, parent__isnull=True)
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]


class CategoryWithChildrenView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True, parent__isnull=True)
    serializer_class = CategoryWithChildrenSerializer
    permission_classes = [AllowAny]


class SubCategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parent__id']

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent__isnull=False)


class AdCreateView(generics.CreateAPIView):
    serializer_class = AdCreateSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.filter(status='active', is_active=True)
    serializer_class = AdDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Ad.objects.filter(id=instance.id).update(view_count=F('view_count') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AdListView(generics.ListAPIView):
    serializer_class = AdListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AdFilter
    search_fields = ['name_uz', 'name_ru', 'description_uz', 'description_ru']
    ordering_fields = ['published_at', 'price', 'view_count']
    ordering = ['-published_at']

    def get_queryset(self):
        return Ad.objects.filter(status='active', is_active=True).select_related('seller', 'category')


class MyAdListView(generics.ListAPIView):
    serializer_class = MyAdSerializer
    permission_classes = [IsSeller]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Ad.objects.none()
        return Ad.objects.filter(seller=self.request.user)


class MyAdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAdDetailSerializer
    permission_classes = [IsSeller, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.role in ['super_admin', 'admin']:
            return Ad.objects.all()
        return Ad.objects.filter(seller=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdUpdateSerializer
        return MyAdDetailSerializer


class FavouriteProductCreateView(generics.CreateAPIView):
    serializer_class = FavouriteProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteProductByIdCreateView(generics.CreateAPIView):
    serializer_class = FavouriteProductByIdSerializer
    permission_classes = [AllowAny]


@extend_schema(
    parameters=[
        OpenApiParameter(name='device_id', type=str, location=OpenApiParameter.QUERY)
    ],
    responses={
        204: OpenApiResponse(description='Favourite product deleted'),
        404: OpenApiResponse(description='Favourite not found'),
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def favourite_product_delete(request, id):
    try:
        favourite = FavouriteProduct.objects.get(product_id=id, user=request.user)
        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except FavouriteProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    parameters=[
        OpenApiParameter(name='device_id', type=str, location=OpenApiParameter.QUERY)
    ],
    responses={
        204: OpenApiResponse(description='Favourite product deleted'),
        404: OpenApiResponse(description='Favourite not found'),
    }
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def favourite_product_by_id_delete(request, id):
    device_id = request.query_params.get('device_id')
    try:
        if device_id:
            favourite = FavouriteProduct.objects.get(product_id=id, device_id=device_id)
        else:
            favourite = FavouriteProduct.objects.get(product_id=id, user=request.user)
        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except FavouriteProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class MyFavouriteProductListView(generics.ListAPIView):
    serializer_class = MyFavouriteProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Ad.objects.none()

        favourites = FavouriteProduct.objects.filter(user=self.request.user)
        return Ad.objects.filter(id__in=favourites.values_list('product_id', flat=True))


class MyFavouriteProductByIdListView(generics.ListAPIView):
    serializer_class = MyFavouriteProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['device_id']

    def get_queryset(self):
        device_id = self.request.query_params.get('device_id')
        if device_id:
            favourites = FavouriteProduct.objects.filter(device_id=device_id)
        else:
            favourites = FavouriteProduct.objects.filter(user=self.request.user)
        return Ad.objects.filter(id__in=favourites.values_list('product_id', flat=True))


class MySearchCreateView(generics.CreateAPIView):
    serializer_class = MySearchCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MySearchListView(generics.ListAPIView):
    serializer_class = MySearchDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return MySearch.objects.none()
        return MySearch.objects.filter(user=self.request.user)


@extend_schema(
    responses={
        204: OpenApiResponse(description='Search deleted'),
        404: OpenApiResponse(description='Search not found'),
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def my_search_delete(request, id):
    try:
        search = MySearch.objects.get(id=id, user=request.user)
        search.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except MySearch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProductImageCreateView(generics.CreateAPIView):
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsSeller]


@extend_schema(
    responses={
        200: OpenApiResponse(response=AdDetailSerializer, description='Product details'),
        404: OpenApiResponse(description='Product not found'),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def product_download(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    serializer = AdDetailSerializer(ad, context={'request': request})
    return Response(serializer.data)


class SearchCategoryProductView(generics.ListAPIView):
    serializer_class = SearchResultSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        results = []

        if query:
            categories = Category.objects.filter(
                Q(name__icontains=query) & Q(is_active=True)
            )[:5]

            for category in categories:
                results.append({
                    'id': category.id,
                    'name': category.name,
                    'type': 'category',
                    'icon': category.icon.url if category.icon else None
                })

            ads = Ad.objects.filter(
                Q(name_uz__icontains=query) | Q(name_ru__icontains=query),
                status='active', is_active=True
            )[:5]

            for ad in ads:
                results.append({
                    'id': ad.id,
                    'name': ad.name,
                    'type': 'product',
                    'icon': ad.category.icon.url if ad.category.icon else None
                })

        return results

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(results, many=True)
        return Response({
            'count': len(results),
            'next': None,
            'previous': None,
            'results': serializer.data
        })


class SearchCompleteView(generics.ListAPIView):
    serializer_class = SearchCompleteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        results = []

        if query:
            ads = Ad.objects.filter(
                Q(name_uz__icontains=query) | Q(name_ru__icontains=query),
                status='active', is_active=True
            )[:10]

            for ad in ads:
                results.append({
                    'id': ad.id,
                    'name': ad.name,
                    'icon': ad.category.icon.url if ad.category.icon else None
                })

        return results

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        serializer = self.get_serializer(results, many=True)
        return Response({
            'count': len(results),
            'next': None,
            'previous': None,
            'results': serializer.data
        })


@extend_schema(
    responses={
        200: OpenApiResponse(description='Search count increased'),
        400: OpenApiResponse(description='Invalid request'),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def search_count_increase(request, id):
    try:
        search_term, created = PopularSearchTerm.objects.get_or_create(
            category_id=id,
            defaults={'name': f'Category {id}', 'search_count': 0}
        )
        search_term.search_count = F('search_count') + 1
        search_term.save()
        search_term.refresh_from_db()

        serializer = PopularSearchIncreaseSerializer(search_term)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PopularSearchTermsView(generics.ListAPIView):
    queryset = PopularSearchTerm.objects.all().order_by('-search_count')
    serializer_class = PopularSearchTermSerializer
    permission_classes = [AllowAny]
