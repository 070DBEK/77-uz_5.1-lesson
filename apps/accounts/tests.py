from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import SellerRegistration
from apps.store.models import Category

User = get_user_model()


class UserModelTest(TestCase):
    """User model tests"""

    def setUp(self):
        self.user_data = {
            'phone_number': '+998901234567',
            'full_name': 'Test User',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """User creation test"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.phone_number, '+998901234567')
        self.assertEqual(user.role, 'customer')
        self.assertFalse(user.is_verified)

    def test_create_superuser(self):
        """Superuser creation test"""
        user = User.objects.create_superuser(**self.user_data)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, 'super_admin')


class AuthenticationAPITest(APITestCase):
    """Authentication API tests"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.user_data = {
            'phone_number': '+998901234567',
            'full_name': 'Test User',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }

    def test_user_registration(self):
        """User registration test"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['user']['role'], 'customer')

    def test_user_login(self):
        """User login test"""
        User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123',
            full_name='Test User'
        )

        login_data = {
            'phone_number': '+998901234567',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_invalid_login(self):
        """Invalid login test"""
        login_data = {
            'phone_number': '+998901234567',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SellerRegistrationAPITest(APITestCase):
    """Seller registration API tests"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123',
            full_name='Test User',
            role='customer'
        )
        self.category = Category.objects.create(name='Test Category')
        self.seller_registration_url = reverse('accounts:seller-registration')

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_seller_registration(self):
        """Seller application test"""
        data = {
            'full_name': 'Test Seller',
            'project_name': 'My Shop',
            'category': self.category.id,
            'phone_number': '+998901234567',
            'address': {'name': 'Tashkent'}
        }
        response = self.client.post(self.seller_registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')

    def test_seller_registration_duplicate(self):
        """Duplicate application test"""
        SellerRegistration.objects.create(
            user=self.user,
            full_name='Test Seller',
            project_name='My Shop',
            category=self.category,
            phone_number='+998901234567',
            address='Tashkent',
            status='pending'
        )

        data = {
            'full_name': 'Test Seller 2',
            'project_name': 'My Shop 2',
            'category': self.category.id,
            'phone_number': '+998901234567',
            'address': {'name': 'Tashkent'}
        }
        response = self.client.post(self.seller_registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminAPITest(APITestCase):
    """Admin API tests"""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            phone_number='+998901111111',
            password='adminpass123',
            full_name='Admin User',
            role='admin'
        )
        self.customer = User.objects.create_user(
            phone_number='+998902222222',
            password='customerpass123',
            full_name='Customer User',
            role='customer'
        )

        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_admin_user_list(self):
        """Admin: users list test"""
        url = reverse('accounts:admin-user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_approve_seller_registration(self):
        """Admin: approve seller registration test"""
        category = Category.objects.create(name='Test Category')
        registration = SellerRegistration.objects.create(
            user=self.customer,
            full_name='Test Seller',
            project_name='My Shop',
            category=category,
            phone_number='+998902222222',
            address='Tashkent',
            status='pending'
        )

        url = reverse('accounts:approve-seller', kwargs={'registration_id': registration.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.role, 'seller')
        self.assertTrue(self.customer.is_verified)


class TokenAPITest(APITestCase):
    """Token API tests"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123',
            full_name='Test User'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)

    def test_token_verify(self):
        """Token verify test"""
        url = reverse('accounts:token-verify')
        data = {'token': self.access_token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        self.assertEqual(int(response.data['user_id']), self.user.id)

    def test_token_refresh(self):
        """Token refresh test"""
        url = reverse('accounts:token-refresh')
        data = {'refresh_token': self.refresh_token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_invalid_token_verify(self):
        """Invalid token verify test"""
        url = reverse('accounts:token-verify')
        data = {'token': 'invalid_token'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['valid'])
