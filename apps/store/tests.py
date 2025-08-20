from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Category, Ad, AdPhoto, FavouriteProduct, MySearch, PopularSearchTerm
from apps.common.models import Region, District

User = get_user_model()


class CategoryModelTest(TestCase):
    """Category model testlari"""

    def setUp(self):
        self.parent_category = Category.objects.create(
            name='Electronics',
            is_active=True
        )
        self.child_category = Category.objects.create(
            name='Phones',
            parent=self.parent_category,
            is_active=True
        )

    def test_category_creation(self):
        """Category yaratish testi"""
        self.assertEqual(self.parent_category.name, 'Electronics')
        self.assertTrue(self.parent_category.is_active)
        self.assertIsNone(self.parent_category.parent)

    def test_child_category(self):
        """Child category testi"""
        self.assertEqual(self.child_category.parent, self.parent_category)
        self.assertIn(self.child_category, self.parent_category.children.all())


class AdModelTest(TestCase):
    """Ad model testlari"""

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123',
            full_name='Test Seller',
            role='seller'
        )
        self.category = Category.objects.create(name='Test Category')
        self.ad = Ad.objects.create(
            seller=self.user,
            category=self.category,
            name_uz='Test mahsulot',
            name_ru='Тестовый товар',
            description_uz='Test tavsifi',
            price=100000,
            status='active'
        )

    def test_ad_creation(self):
        """Ad yaratish testi"""
        self.assertEqual(self.ad.seller, self.user)
        self.assertEqual(self.ad.category, self.category)
        self.assertEqual(self.ad.price, 100000)
        self.assertTrue(self.ad.slug)  # Slug avtomatik yaratiladi

    def test_ad_name_property(self):
        """Ad name property testi"""
        self.assertEqual(self.ad.name, 'Test mahsulot')


class CategoryAPITest(APITestCase):
    """Category API testlari"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics', is_active=True)
        self.subcategory = Category.objects.create(
            name='Phones',
            parent=self.category,
            is_active=True
        )

    def test_category_list(self):
        """Category list API testi"""
        url = reverse('store:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_categories_with_children(self):
        """Categories with children API testi"""
        url = reverse('store:categories-with-children')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Parent category children bor ekanligini tekshirish
        parent_data = next(cat for cat in response.data['results'] if cat['id'] == self.category.id)
        self.assertGreater(len(parent_data['children']), 0)


class AdAPITest(APITestCase):
    """Ad API testlari"""

    def setUp(self):
        self.client = APIClient()
        self.seller = User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123',
            full_name='Test Seller',
            role='seller'
        )
        self.customer = User.objects.create_user(
            phone_number='+998902222222',
            password='customerpass123',
            full_name='Test Customer',
            role='customer'
        )
        self.category = Category.objects.create(name='Test Category')
        self.ad = Ad.objects.create(
            seller=self.seller,
            category=self.category,
            name_uz='Test mahsulot',
            price=100000,
            status='active'
        )

    def test_ad_list_public(self):
        """Public ad list testi"""
        url = reverse('store:ad-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_ad_detail_public(self):
        """Public ad detail testi"""
        url = reverse('store:ad-detail', kwargs={'slug': self.ad.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.ad.id)

    def test_ad_create_seller(self):
        """Seller ad yaratish testi"""
        refresh = RefreshToken.for_user(self.seller)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = reverse('store:ad-create')
        data = {
            'name_uz': 'Yangi mahsulot',
            'name_ru': 'Новый товар',
            'category': self.category.id,
            'description_uz': 'Tavsif',
            'price': 200000,
            'photos': ['http://example.com/photo1.jpg']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ad_create_customer_forbidden(self):
        """Customer ad yarata olmasligi testi"""
        refresh = RefreshToken.for_user(self.customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = reverse('store:ad-create')
        data = {
            'name_uz': 'Yangi mahsulot',
            'category': self.category.id,
            'price': 200000,
            'photos': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FavouriteAPITest(APITestCase):
    """Favourite API testlari"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123',
            full_name='Test User'
        )
        self.seller = User.objects.create_user(
            phone_number='+998902222222',
            password='sellerpass123',
            full_name='Test Seller',
            role='seller'
        )
        self.category = Category.objects.create(name='Test Category')
        self.ad = Ad.objects.create(
            seller=self.seller,
            category=self.category,
            name_uz='Test mahsulot',
            price=100000,
            status='active'
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_add_to_favourites(self):
        """Sevimlilar ro'yxatiga qo'shish testi"""
        url = reverse('store:favourite-create')
        data = {'product': self.ad.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Favourite yaratilganligini tekshirish
        self.assertTrue(
            FavouriteProduct.objects.filter(user=self.user, product=self.ad).exists()
        )

    def test_my_favourites_list(self):
        """Mening sevimlilarim ro'yxati testi"""
        # Avval favourite qo'shish
        FavouriteProduct.objects.create(user=self.user, product=self.ad)

        url = reverse('store:my-favourite-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)


class SearchAPITest(APITestCase):
    """Search API testlari"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics')
        self.seller = User.objects.create_user(
            phone_number='+998901234567',
            password='testpass123',
            full_name='Test Seller',
            role='seller'
        )
        self.ad = Ad.objects.create(
            seller=self.seller,
            category=self.category,
            name_uz='iPhone 15',
            name_ru='Айфон 15',
            price=1000000,
            status='active'
        )

    def test_search_category_product(self):
        """Category va product qidiruv testi"""
        url = reverse('store:search-category-product')
        response = self.client.get(url, {'q': 'iPhone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_search_complete(self):
        """Search complete testi"""
        url = reverse('store:search-complete')
        response = self.client.get(url, {'q': 'iPhone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_popular_search_terms(self):
        """Popular search terms testi"""
        PopularSearchTerm.objects.create(
            name='iPhone',
            search_count=100,
            category=self.category
        )

        url = reverse('store:search-populars')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
