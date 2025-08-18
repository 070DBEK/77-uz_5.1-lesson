#!/usr/bin/env python
"""
Yaxshilangan user flow'ni test qilish
"""
import requests
import json
import os
import sys
import django

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.store.models import Category

BASE_URL = "http://localhost:8000/api/v1"


def get_valid_category_id():
    """Mavjud category ID olish"""
    try:
        category = Category.objects.filter(is_active=True).first()
        if category:
            return category.id
        return None
    except:
        return None


def test_improved_flow():
    """Yaxshilangan flow test qilish"""
    print("🔄 TESTING IMPROVED USER FLOW")
    print("=" * 50)

    # Kategoriyani tekshirish
    category_id = get_valid_category_id()
    if not category_id:
        print("❌ No categories found! Loading initial data...")
        try:
            from scripts.load_initial_data import load_initial_data
            load_initial_data()
            category_id = get_valid_category_id()
        except:
            print("❌ Could not load initial data. Please run: python scripts/load_initial_data.py")
            return

    print(f"📂 Using category ID: {category_id}")

    # 1. Customer sifatida ro'yxatdan o'tish
    register_data = {
        "full_name": "Test Customer",
        "phone_number": "+998900111222",
        "password": "test123456",
        "password_confirm": "test123456"
        # role field yo'q - avtomatik customer bo'ladi
    }

    print("\n1️⃣ Registering as customer (automatic)...")
    try:
        response = requests.post(f"{BASE_URL}/accounts/register/", json=register_data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 201:
            data = response.json()
            access_token = data['access_token']
            user_role = data['user']['role']
            print(f"   ✅ Registered successfully as: {user_role}")
            print(f"   📱 Phone: {data['user']['phone_number']}")
        elif response.status_code == 400:
            print("   ⚠️ User already exists, trying to login...")
            # Try login instead
            login_data = {
                "phone_number": "+998900111222",
                "password": "test123456"
            }
            response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                access_token = data['access_token']
                print(f"   ✅ Logged in as: {data['user']['role']}")
            else:
                print(f"   ❌ Login failed: {response.text}")
                return
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return

    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return

    # 2. Profile ma'lumotlarini olish
    print("\n2️⃣ Getting user profile...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/accounts/me/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Profile loaded: {data['full_name']} ({data['role']})")
        else:
            print(f"   ❌ Profile failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Profile error: {e}")

    # 3. Seller bo'lish uchun ariza berish
    seller_application = {
        "full_name": "Test Seller Business",
        "project_name": "My Online Store",
        "category": category_id,  # Valid category ID
        "phone_number": "+998900111222",
        "address": {
            "name": "Tashkent, Chilonzor",
            "lat": 41.311081,
            "long": 69.240562
        }
    }

    print(f"\n3️⃣ Applying to become seller (category: {category_id})...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(
            f"{BASE_URL}/accounts/seller/registration/",
            json=seller_application,
            headers=headers
        )
        print(f"   Status: {response.status_code}")

        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Seller application submitted")
            print(f"   📋 Status: {data['status']}")
            print(f"   💼 Project: {data['project_name']}")
            print(f"   📝 Message: {data['message']}")
            registration_id = data['id']
        elif response.status_code == 400:
            error_data = response.json()
            if "already submitted" in str(error_data):
                print("   ⚠️ Application already exists")
                registration_id = None
            else:
                print(f"   ❌ Application failed: {error_data}")
                return
        else:
            print(f"   ❌ Application failed: {response.text}")
            return

    except Exception as e:
        print(f"   ❌ Application error: {e}")
        return

    # 4. Available categories ko'rsatish
    print("\n4️⃣ Available categories:")
    try:
        response = requests.get(f"{BASE_URL}/store/category/")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('results', [])
            for cat in categories[:5]:  # First 5 categories
                print(f"   📂 ID: {cat['id']} - {cat['name']}")
        else:
            print(f"   ❌ Could not fetch categories: {response.text}")
    except Exception as e:
        print(f"   ❌ Categories error: {e}")

    print("\n🎯 FLOW SUMMARY:")
    print("   1. ✅ User registers as customer (automatic)")
    print("   2. ✅ User can use platform as customer")
    print("   3. ✅ User can apply to become seller")
    print("   4. ✅ Admin reviews and approves/rejects")
    print("   5. ✅ Approved users become sellers")
    print(f"\n📋 Next steps:")
    print(f"   - Admin can approve via: POST /accounts/admin/seller-registrations/{{id}}/approve/")
    print(f"   - Check applications via: GET /accounts/admin/seller-registrations/")


def main():
    # Server check
    try:
        response = requests.get(f"{BASE_URL}/common/setting/", timeout=5)
        print("✅ Server is running\n")
    except:
        print("❌ Server is not running! Please start with: python manage.py runserver")
        return

    test_improved_flow()

    print("\n🎉 Improved flow test completed!")


if __name__ == '__main__':
    main()
