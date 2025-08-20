from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Region, District, StaticPage, Setting


class RegionModelTest(TestCase):
    """Region model testlari"""

    def setUp(self):
        self.region = Region.objects.create(name='Toshkent shahar')
        self.district = District.objects.create(
            region=self.region,
            name='Chilonzor tumani'
        )

    def test_region_creation(self):
        """Region yaratish testi"""
        self.assertEqual(self.region.name, 'Toshkent shahar')
        self.assertTrue(self.region.created_at)

    def test_district_creation(self):
        """District yaratish testi"""
        self.assertEqual(self.district.region, self.region)
        self.assertEqual(self.district.name, 'Chilonzor tumani')


class CommonAPITest(APITestCase):
    """Common API testlari"""

    def setUp(self):
        self.client = APIClient()
        self.region = Region.objects.create(name='Toshkent shahar')
        self.district = District.objects.create(
            region=self.region,
            name='Chilonzor tumani'
        )
        self.static_page = StaticPage.objects.create(
            slug='about-us',
            title='Biz haqimizda',
            content='Test content'
        )
        self.setting = Setting.objects.create(
            phone='+998712345678',
            support_email='support@77.uz',
            app_version='1.0.0'
        )

    def test_regions_with_districts(self):
        """Regions with districts API testi"""
        url = reverse('common:regions-with-districts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

        # District mavjudligini tekshirish
        region_data = response.data['results'][0]
        self.assertIn('districts', region_data)
        self.assertGreaterEqual(len(region_data['districts']), 1)

    def test_static_pages_list(self):
        """Static pages list API testi"""
        url = reverse('common:static-pages-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_static_page_detail(self):
        """Static page detail API testi"""
        url = reverse('common:static-page-detail', kwargs={'slug': 'about-us'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], 'about-us')
        self.assertEqual(response.data['title'], 'Biz haqimizda')

    def test_settings(self):
        """Settings API testi"""
        url = reverse('common:setting')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+998712345678')
        self.assertEqual(response.data['app_version'], '1.0.0')
