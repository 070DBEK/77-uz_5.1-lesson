#!/usr/bin/env python
"""
Har bir rol uchun request/response test qilish
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


class RoleBasedTester:
    def __init__(self):
        self.tokens = {}
        self.users = {}

    def register_and_login_users(self):
        """Har xil rol uchun user'lar yaratish va login qilish"""
        print("👥 Creating and logging in users for each role...")

        # Customer
        customer_data = {
            "full_name": "Test Customer",
            "phone_number": "+998900000001",
            "password": "test123",
            "password_confirm": "test123"
        }

        try:
            response = requests.post(f"{BASE_URL}/accounts/register/", json=customer_data)
            if response.status_code == 201:
                data = response.json()
                self.tokens['customer'] = data['access_token']
                self.users['customer'] = data['user']
                print("✅ Customer registered and logged in")
        except Exception as e:
            print(f"❌ Customer registration failed: {e}")

        # Seller (need to create and approve)
        seller_data = {
            "full_name": "Test Seller",
            "phone_number": "+998900000002",
            "password": "test123",
            "password_confirm": "test123"
        }

        try:
            response = requests.post(f"{BASE_URL}/accounts/register/", json=seller_data)
            if response.status_code == 201:
                data = response.json()
                # Seller registration
                seller_reg_data = {
                    "full_name": "Test Seller",
                    "project_name": "Test Shop",
                    "category": 1,
                    "phone_number": "+998900000002",
                    "address": {
                        "name": "Test Address",
                        "lat": 41.311081,
                        "long": 69.240562
                    }
                }
                headers = {"Authorization": f"Bearer {data['access_token']}"}
                reg_response = requests.post(f"{BASE_URL}/accounts/seller/registration/",
                                             json=seller_reg_data, headers=headers)

                self.tokens['seller'] = data['access_token']
                self.users['seller'] = data['user']
                print("✅ Seller registered (pending approval)")
        except Exception as e:
            print(f"❌ Seller registration failed: {e}")

    def test_public_endpoints(self):
        """Public endpoints test qilish"""
        print("\n🌐 Testing Public Endpoints...")

        endpoints = [
            ("GET", "/common/setting/", None),
            ("GET", "/common/pages/", None),
            ("GET", "/common/regions-with-districts/", None),
            ("GET", "/store/category/", None),
            ("GET", "/store/list/ads/", None),
            ("GET", "/store/search/populars/", None),
        ]

        for method, endpoint, data in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{BASE_URL}{endpoint}")
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}", json=data)

                status = "✅" if response.status_code == 200 else "❌"
                print(f"   {status} {method} {endpoint} - {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    print(f"      📊 Response keys: {list(data.keys())}")

            except Exception as e:
                print(f"   ❌ {method} {endpoint} - Error: {e}")

    def test_customer_endpoints(self):
        """Customer endpoints test qilish"""
        print("\n👤 Testing Customer Endpoints...")

        if 'customer' not in self.tokens:
            print("   ❌ No customer token available")
            return

        headers = {"Authorization": f"Bearer {self.tokens['customer']}"}

        endpoints = [
            ("GET", "/accounts/me/", None),
            ("GET", "/store/my-favourite-product/", None),
            ("POST", "/store/favourite-product-create/", {"product": 1}),
            ("POST", "/store/my-search/", {
                "category": 1,
                "search_query": "test",
                "price_min": 100000,
                "price_max": 1000000
            }),
        ]

        for method, endpoint, data in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)

                status = "✅" if response.status_code in [200, 201] else "❌"
                print(f"   {status} {method} {endpoint} - {response.status_code}")

                if response.status_code in [200, 201]:
                    resp_data = response.json()
                    print(f"      📊 Response: {json.dumps(resp_data, indent=2)[:200]}...")

            except Exception as e:
                print(f"   ❌ {method} {endpoint} - Error: {e}")

    def test_seller_endpoints(self):
        """Seller endpoints test qilish"""
        print("\n🏪 Testing Seller Endpoints...")

        if 'seller' not in self.tokens:
            print("   ❌ No seller token available")
            return

        headers = {"Authorization": f"Bearer {self.tokens['seller']}"}

        endpoints = [
            ("GET", "/accounts/me/", None),
            ("GET", "/store/my-ads/", None),
            ("POST", "/store/ads/", {
                "name_uz": "Test Product",
                "name_ru": "Test Product",
                "category": 1,
                "description_uz": "Test description",
                "description_ru": "Test description",
                "price": 100000,
                "photos": ["https://example.com/photo.jpg"]
            }),
        ]

        for method, endpoint, data in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)

                status = "✅" if response.status_code in [200, 201] else "❌"
                print(f"   {status} {method} {endpoint} - {response.status_code}")

                if response.status_code in [200, 201]:
                    resp_data = response.json()
                    print(f"      📊 Response: {json.dumps(resp_data, indent=2)[:200]}...")
                elif response.status_code == 403:
                    print(f"      🔒 Permission denied (expected for some roles)")

            except Exception as e:
                print(f"   ❌ {method} {endpoint} - Error: {e}")

    def test_permission_errors(self):
        """Permission xatoliklarini test qilish"""
        print("\n🔒 Testing Permission Errors...")

        # Customer trying to access seller endpoints
        if 'customer' in self.tokens:
            headers = {"Authorization": f"Bearer {self.tokens['customer']}"}

            try:
                response = requests.get(f"{BASE_URL}/store/my-ads/", headers=headers)
                if response.status_code == 403:
                    print("   ✅ Customer correctly denied access to seller endpoints")
                else:
                    print(f"   ❌ Customer should be denied access: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error testing customer permissions: {e}")

        # Unauthenticated trying to access protected endpoints
        try:
            response = requests.get(f"{BASE_URL}/accounts/me/")
            if response.status_code == 401:
                print("   ✅ Unauthenticated correctly denied access")
            else:
                print(f"   ❌ Should require authentication: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error testing unauthenticated access: {e}")

    def run_all_tests(self):
        """Barcha testlarni ishga tushirish"""
        print("🧪 ROLE-BASED API TESTING")
        print("=" * 50)

        self.register_and_login_users()
        self.test_public_endpoints()
        self.test_customer_endpoints()
        self.test_seller_endpoints()
        self.test_permission_errors()

        print("\n🎉 Role-based testing completed!")


def main():
    print("Make sure the server is running: python manage.py runserver")

    # Server check
    try:
        response = requests.get(f"{BASE_URL}/common/setting/", timeout=5)
        print("✅ Server is running\n")
    except:
        print("❌ Server is not running! Please start with: python manage.py runserver")
        return

    tester = RoleBasedTester()
    tester.run_all_tests()


if __name__ == '__main__':
    main()

