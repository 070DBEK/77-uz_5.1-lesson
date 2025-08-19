from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that doesn't fail on missing tokens
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            # No token provided, return None (not authenticated)
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except TokenError:
            # Invalid token, but don't raise exception
            # Let the view handle authentication requirements
            return None

    def authenticate_header(self, request):
        return 'Bearer'
