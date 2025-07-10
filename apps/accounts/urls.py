from django.urls import path
from . import views


urlpatterns = [
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    path('edit/', views.UserProfileEditView.as_view(), name='user-profile-edit'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('seller/registration/', views.seller_registration_view, name='seller-registration'),
    path('token/refresh/', views.token_refresh_view, name='token-refresh'),
    path('token/verify/', views.token_verify_view, name='token-verify'),
]
