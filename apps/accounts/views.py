from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django.contrib.auth import authenticate

from .models import User, SellerRegistration
from .permissions import IsSuperAdmin, IsAdmin, CanManageSellers, CanApplyForSeller
from .serializers import (
    UserProfileSerializer, UserProfileEditSerializer, UserLoginSerializer,
    UserRegisterSerializer, LoginResponseSerializer, SellerRegistrationSerializer,
    TokenRefreshSerializer, TokenVerifySerializer, UserListSerializer,
    SellerRegistrationListSerializer
)
from .debug_views import debug_user_info, force_refresh_user


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileEditView(generics.UpdateAPIView):
    serializer_class = UserProfileEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# Admin endpoints
class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()

        if self.request.user.role == 'super_admin':
            return User.objects.all()
        else:
            return User.objects.exclude(role='super_admin')


class SellerRegistrationListView(generics.ListAPIView):
    queryset = SellerRegistration.objects.all()
    serializer_class = SellerRegistrationListSerializer
    permission_classes = [CanManageSellers]


@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(description='Seller registration approved'),
        404: OpenApiResponse(description='Registration not found'),
    }
)
@api_view(['POST'])
@permission_classes([CanManageSellers])
def approve_seller_registration(request, registration_id):
    try:
        registration = SellerRegistration.objects.get(id=registration_id)

        registration.status = 'approved'
        registration.save()

        user = registration.user
        user.role = 'seller'
        user.is_verified = True
        user.save()

        # Refresh from database to confirm changes
        user.refresh_from_db()

        return Response({
            'message': 'Seller registration approved successfully',
            'user_id': user.id,
            'old_role': 'customer',
            'new_role': user.role,
            'is_verified': user.is_verified,
            'registration_status': registration.status
        })
    except SellerRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=404)
    except Exception as e:
        return Response({'error': f'Error approving registration: {str(e)}'}, status=500)


@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(description='Seller registration rejected'),
        404: OpenApiResponse(description='Registration not found'),
    }
)
@api_view(['POST'])
@permission_classes([CanManageSellers])
def reject_seller_registration(request, registration_id):
    try:
        registration = SellerRegistration.objects.get(id=registration_id)
        registration.status = 'rejected'
        registration.save()

        user = registration.user
        if user.role != 'customer':
            user.role = 'customer'
            user.is_verified = False
            user.save()
            user.refresh_from_db()

        return Response({
            'message': 'Seller registration rejected',
            'user_id': user.id,
            'current_role': user.role,
            'is_verified': user.is_verified,
            'registration_status': registration.status
        })
    except SellerRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=404)
    except Exception as e:
        return Response({'error': f'Error rejecting registration: {str(e)}'}, status=500)


@extend_schema(
    request=UserRegisterSerializer,
    responses={
        201: OpenApiResponse(response=LoginResponseSerializer, description='Admin user created'),
        400: OpenApiResponse(description='Invalid data'),
    }
)
@api_view(['POST'])
@permission_classes([IsSuperAdmin])
def create_admin_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.role = 'admin'
        user.save()

        return Response({
            'message': 'Admin user created successfully',
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Public endpoints
@extend_schema(
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(response=LoginResponseSerializer, description='Successful login'),
        400: OpenApiResponse(description='Invalid credentials'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint - PUBLIC"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserRegisterSerializer,
    responses={
        201: OpenApiResponse(response=LoginResponseSerializer, description='Successful registration'),
        400: OpenApiResponse(description='Invalid data'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register endpoint - Har doim customer sifatida ro'yxatdan o'tish"""
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SellerRegistrationSerializer,
    responses={
        201: OpenApiResponse(description='Seller registration submitted'),
        400: OpenApiResponse(description='Invalid data'),
    }
)
@api_view(['POST'])
@permission_classes([CanApplyForSeller])
def seller_registration_view(request):
    serializer = SellerRegistrationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        registration = serializer.save()
        return Response({
            'id': registration.id,
            'full_name': registration.full_name,
            'project_name': registration.project_name,
            'category_id': registration.category.id if registration.category else None,
            'phone_number': registration.phone_number,
            'address': registration.address,
            'status': registration.status,
            'message': 'Seller application submitted successfully. Please wait for admin approval.',
            'created_at': registration.created_at
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=TokenRefreshSerializer,
    responses={
        200: OpenApiResponse(description='Token refreshed successfully'),
        400: OpenApiResponse(description='Invalid refresh token'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access_token': str(refresh.access_token)
        })
    except TokenError:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=TokenVerifySerializer,
    responses={
        200: OpenApiResponse(description='Token is valid'),
        400: OpenApiResponse(description='Invalid token'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def token_verify_view(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from rest_framework_simplejwt.tokens import UntypedToken
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from django.contrib.auth import get_user_model

        User = get_user_model()
        UntypedToken(token)

        from rest_framework_simplejwt.tokens import AccessToken
        access_token = AccessToken(token)
        user_id = access_token.payload.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            return Response({
                'valid': True,
                'user_id': user_id,
                'user_role': user.role
            })
        except User.DoesNotExist:
            return Response({'valid': False, 'error': 'User not found'}, status=400)

    except (InvalidToken, TokenError):
        return Response({'valid': False, 'error': 'Invalid token'}, status=400)


# Debug endpoints
@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(description='User info retrieved'),
        404: OpenApiResponse(description='User not found'),
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_user_info_view(request):
    """Debug: User info"""
    return debug_user_info(request)


@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(description='User refreshed'),
        404: OpenApiResponse(description='User not found'),
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def force_refresh_user_view(request):
    """Debug: Force refresh user"""
    return force_refresh_user(request)
