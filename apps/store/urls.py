from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('categories-with-childs/', views.CategoryWithChildrenView.as_view(), name='categories-with-children'),
    path('sub-category/', views.SubCategoryListView.as_view(), name='sub-category-list'),

    # Ads
    path('ads/', views.AdCreateView.as_view(), name='ad-create'),
    path('ads/<slug:slug>/', views.AdDetailView.as_view(), name='ad-detail'),
    path('list/ads/', views.AdListView.as_view(), name='ad-list'),

    # My Ads
    path('my-ads/', views.MyAdListView.as_view(), name='my-ad-list'),
    path('my-ads/<int:pk>/', views.MyAdDetailView.as_view(), name='my-ad-detail'),

    # Favourites
    path('favourite-product-create/', views.FavouriteProductCreateView.as_view(), name='favourite-create'),
    path('favourite-product-create-by-id/', views.FavouriteProductByIdCreateView.as_view(),
         name='favourite-create-by-id'),
    path('favourite-product/<int:id>/delete/', views.favourite_product_delete, name='favourite-delete'),
    path('favourite-product-by-id/<int:id>/delete/', views.favourite_product_by_id_delete,
         name='favourite-delete-by-id'),
    path('my-favourite-product/', views.MyFavouriteProductListView.as_view(), name='my-favourite-list'),
    path('my-favourite-product-by-id/', views.MyFavouriteProductByIdListView.as_view(), name='my-favourite-by-id-list'),

    # Saved Searches
    path('my-search/', views.MySearchCreateView.as_view(), name='my-search-create'),
    path('my-search/list/', views.MySearchListView.as_view(), name='my-search-list'),
    path('my-search/<int:id>/delete/', views.my_search_delete, name='my-search-delete'),

    # Product Images
    path('product-image-create/', views.ProductImageCreateView.as_view(), name='product-image-create'),
    path('product-download/<slug:slug>/', views.product_download, name='product-download'),

    # Search
    path('search/category-product/', views.SearchCategoryProductView.as_view(), name='search-category-product'),
    path('search/complete/', views.SearchCompleteView.as_view(), name='search-complete'),
    path('search/count-increase/<int:id>/', views.search_count_increase, name='search-count-increase'),
    path('search/populars/', views.PopularSearchTermsView.as_view(), name='search-populars'),
]
