import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.store.models import Category, Ad

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        phone_number='+998901234567',
        password='testpass123',
        role='seller'
    )

@pytest.fixture
def category():
    return Category.objects.create(name='Electronics')

@pytest.mark.django_db
class TestAdCreation:
    def test_create_ad_success(self, api_client, user, category):
        api_client.force_authenticate(user=user)

        url = reverse('ad-create')
        data = {
            'name_uz': 'Test Product',
            'category': category.id,
            'description_uz': 'Test description',
            'price': 100000,
            'photos': ['http://example.com/photo1.jpg']
        }

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Ad.objects.filter(name_uz='Test Product').exists()

    def test_create_ad_unauthorized(self, api_client, category):
        url = reverse('ad-create')
        data = {
            'name_uz': 'Test Product',
            'category': category.id,
            'price': 100000,
            'photos': []
        }

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestCategoryList:
    def test_category_list(self, api_client):
        Category.objects.create(name='Electronics', is_active=True)
        Category.objects.create(name='Clothing', is_active=True)

        url = reverse('category-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
