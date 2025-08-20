from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, SellerRegistration


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_user_info(request):
    """Debug user information"""
    user = request.user

    try:
        seller_registration = SellerRegistration.objects.get(user=user)
        registration_data = {
            'id': seller_registration.id,
            'status': seller_registration.status,
            'full_name': seller_registration.full_name,
            'project_name': seller_registration.project_name,
            'created_at': seller_registration.created_at
        }
    except SellerRegistration.DoesNotExist:
        registration_data = None

    return Response({
        'user_id': user.id,
        'phone_number': user.phone_number,
        'full_name': user.full_name,
        'role': user.role,
        'is_verified': user.is_verified,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
        'seller_registration': registration_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def force_refresh_user(request):
    """Force refresh user data"""
    user = request.user
    user.refresh_from_db()

    return Response({
        'message': 'User data refreshed',
        'user_id': user.id,
        'role': user.role,
        'is_verified': user.is_verified
    })
