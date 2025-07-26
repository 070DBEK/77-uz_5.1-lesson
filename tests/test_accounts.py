import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'full_name': 'Test User',
        'phone_number': '+998901234567',
        'password': 'testpass123',
        'password_confirm': 'testpass123'
    }


@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registration_success(self, api_client, user_data):
        url = reverse('register')
        response = api_client.post(url, user_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data
        assert User.objects.filter(phone_number=user_data['phone_number']).exists()

    def test_user_registration_password_mismatch(self, api_client, user_data):
        user_data['password_confirm'] = 'different_password'
        url = reverse('register')
        response = api_client.post(url, user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    def test_user_login_success(self, api_client):
        user = User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123'
        )

        url = reverse('login')
        response = api_client.post(url, {
            'phone_number': '+998901234567',
            'password': 'testpass123'
        })

        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data

    def test_user_login_invalid_credentials(self, api_client):
        url = reverse('login')
        response = api_client.post(url, {
            'phone_number': '+998901234567',
            'password': 'wrongpassword'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
