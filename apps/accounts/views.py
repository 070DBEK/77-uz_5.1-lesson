from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django.contrib.auth import authenticate

from .models import User, SellerRegistration
from .permissions import IsSuperAdmin, IsAdmin, CanManageSellers
from .serializers import (
    UserProfileSerializer, UserProfileEditSerializer, UserLoginSerializer,
    UserRegisterSerializer, LoginResponseSerializer, SellerRegistrationSerializer,
    TokenRefreshSerializer, TokenVerifySerializer, UserListSerializer,
    SellerRegistrationListSerializer
)


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
    """Admin: Barcha foydalanuvchilar ro'yxati"""
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        # Swagger uchun fake view check
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()

        if self.request.user.role == 'super_admin':
            return User.objects.all()
        else:  # admin
            return User.objects.exclude(role='super_admin')


class SellerRegistrationListView(generics.ListAPIView):
    """Admin: Sotuvchi arizalari ro'yxati"""
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
    """Admin: Sotuvchi arizasini tasdiqlash"""
    try:
        registration = SellerRegistration.objects.get(id=registration_id)
        registration.status = 'approved'
        registration.save()

        # User rolini seller qilish
        registration.user.role = 'seller'
        registration.user.save()

        return Response({'message': 'Seller registration approved'})
    except SellerRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=404)


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
    """Admin: Sotuvchi arizasini rad etish"""
    try:
        registration = SellerRegistration.objects.get(id=registration_id)
        registration.status = 'rejected'
        registration.save()

        return Response({'message': 'Seller registration rejected'})
    except SellerRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=404)


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
    """Super Admin: Admin foydalanuvchi yaratish"""
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
        401: OpenApiResponse(description='Invalid credentials'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserProfileSerializer(user).data
        })
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
@permission_classes([IsAuthenticated])
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
        refresh = RefreshToken(token)
        return Response({
            'valid': True,
            'user_id': refresh.payload.get('user_id')
        })
    except TokenError:
        return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)
