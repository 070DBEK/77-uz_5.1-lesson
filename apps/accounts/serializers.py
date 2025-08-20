from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Address, SellerRegistration


class UserProfileSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'profile_photo', 'role', 'address', 'created_at']
        read_only_fields = ['id', 'role', 'created_at']

    def get_address(self, obj):
        address = obj.addresses.filter(is_default=True).first()
        if address:
            return {
                'name': address.name,
                'lat': address.lat,
                'long': address.long
            }
        return None


class UserListSerializer(serializers.ModelSerializer):
    """Admin user list"""

    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'role', 'is_verified', 'created_at']


class UserProfileEditSerializer(serializers.ModelSerializer):
    address = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'profile_photo', 'address']

    def update(self, instance, validated_data):
        address_id = validated_data.pop('address', None)

        if address_id:
            try:
                address = Address.objects.get(id=address_id, user=instance)
                instance.addresses.update(is_default=False)
                address.is_default = True
                address.save()
            except Address.DoesNotExist:
                pass

        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(username=phone_number, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include phone_number and password')


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['role'] = 'customer'
        user = User.objects.create_user(**validated_data)
        return user


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserProfileSerializer()


class SellerRegistrationSerializer(serializers.ModelSerializer):
    address = serializers.JSONField()

    class Meta:
        model = SellerRegistration
        fields = ['full_name', 'project_name', 'category', 'phone_number', 'address']

    def validate(self, attrs):
        user = self.context['request'].user
        if user.role != 'customer':
            raise serializers.ValidationError("Only customers can apply to become sellers")

        if SellerRegistration.objects.filter(user=user, status__in=['pending', 'approved']).exists():
            raise serializers.ValidationError(
                "You have already submitted a seller application or you are already a seller")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        address_data = validated_data.pop('address')

        address_str = f"{address_data.get('name', '')}"
        validated_data['address'] = address_str
        validated_data['user'] = user

        return super().create(validated_data)


class SellerRegistrationListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = SellerRegistration
        fields = ['id', 'user', 'full_name', 'project_name', 'category', 'phone_number', 'address', 'status',
                  'created_at']


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
