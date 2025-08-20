from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.openapi import AutoSchema
from rest_framework import serializers


# Error response serializers
class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
    detail = serializers.CharField(required=False)


class ValidationErrorSerializer(serializers.Serializer):
    field_name = serializers.ListField(child=serializers.CharField())


# Success response serializers
class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class PaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()


# Swagger decorators
def auth_swagger_schema(method='POST', summary='', description='', request_serializer=None, responses=None):
    """Authentication endpoint'lari uchun umumiy schema"""
    default_responses = {
        400: OpenApiResponse(response=ValidationErrorSerializer, description='Validation errors'),
        500: OpenApiResponse(response=ErrorResponseSerializer, description='Server error'),
    }
    if responses:
        default_responses.update(responses)

    return extend_schema(
        method=method,
        summary=summary,
        description=description,
        request=request_serializer,
        responses=default_responses,
        tags=['Authentication']
    )


def admin_swagger_schema(method='GET', summary='', description='', responses=None):
    """Admin endpoint'lari uchun umumiy schema"""
    default_responses = {
        401: OpenApiResponse(response=ErrorResponseSerializer, description='Authentication required'),
        403: OpenApiResponse(response=ErrorResponseSerializer, description='Permission denied'),
        404: OpenApiResponse(response=ErrorResponseSerializer, description='Not found'),
    }
    if responses:
        default_responses.update(responses)

    return extend_schema(
        method=method,
        summary=summary,
        description=description,
        responses=default_responses,
        tags=['Admin']
    )
