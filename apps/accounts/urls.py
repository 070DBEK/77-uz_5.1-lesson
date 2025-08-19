from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('token/refresh/', views.token_refresh_view, name='token-refresh'),
    path('token/verify/', views.token_verify_view, name='token-verify'),

    # Authenticated user endpoints
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    path('edit/', views.UserProfileEditView.as_view(), name='user-profile-edit'),
    path('seller/registration/', views.seller_registration_view, name='seller-registration'),

    # Debug endpoints
    path('debug/user-info/', views.debug_user_info, name='debug-user-info'),
    path('debug/refresh-user/', views.force_refresh_user, name='force-refresh-user'),

    # Admin endpoints
    path('admin/users/', views.UserListView.as_view(), name='admin-user-list'),
    path(
        'admin/seller-registrations/',
        views.SellerRegistrationListView.as_view(),
        name='admin-seller-registrations'
    ),
    path(
        'admin/seller-registrations/<int:registration_id>/approve/'
        , views.approve_seller_registration,
         name='approve-seller'
    ),
    path(
        'admin/seller-registrations/<int:registration_id>/reject/',
        views.reject_seller_registration,
         name='reject-seller'
    ),

    # Super Admin endpoints
    path('super-admin/create-admin/', views.create_admin_user, name='create-admin'),
]
