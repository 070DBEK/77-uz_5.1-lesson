#!/usr/bin/env python
"""
Login endpoint'ni test qilish
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_login():
    """Login test qilish"""
    print("🔐 Testing Login Endpoint...")

    # 1. Avval user yaratish
    register_data = {
        "full_name": "Test User",
        "phone_number": "+998901234567",
        "password": "test123456",
        "password_confirm": "test123456",
        "role": "customer"
    }

    try:
        print("\n1️⃣ Registering user...")
        response = requests.post(f"{BASE_URL}/accounts/register/", json=register_data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 201:
            print("   ✅ User registered successfully")
            data = response.json()
            print(f"   📱 Phone: {data['user']['phone_number']}")
            print(f"   🎭 Role: {data['user']['role']}")
        elif response.status_code == 400:
            print("   ⚠️ User already exists (that's OK)")
        else:
            print(f"   ❌ Registration failed: {response.text}")

    except Exception as e:
        print(f"   ❌ Registration error: {e}")

    # 2. Login test qilish
    login_data = {
        "phone_number": "+998901234567",
        "password": "test123456"
    }

    try:
        print("\n2️⃣ Testing login...")
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            print("   ✅ Login successful!")
            data = response.json()
            print(f"   🔑 Access Token: {data['access_token'][:50]}...")
            print(f"   🔄 Refresh Token: {data['refresh_token'][:50]}...")
            print(f"   👤 User: {data['user']['full_name']}")

            # Token bilan protected endpoint test qilish
            headers = {"Authorization": f"Bearer {data['access_token']}"}
            profile_response = requests.get(f"{BASE_URL}/accounts/me/", headers=headers)

            if profile_response.status_code == 200:
                print("   ✅ Token works for protected endpoints!")
                profile_data = profile_response.json()
                print(f"   📋 Profile: {profile_data['full_name']} ({profile_data['role']})")
            else:
                print(f"   ❌ Token doesn't work: {profile_response.status_code}")

        else:
            print(f"   ❌ Login failed: {response.text}")

    except Exception as e:
        print(f"   ❌ Login error: {e}")

    # 3. Noto'g'ri login test qilish
    wrong_login_data = {
        "phone_number": "+998901234567",
        "password": "wrongpassword"
    }

    try:
        print("\n3️⃣ Testing wrong credentials...")
        response = requests.post(f"{BASE_URL}/accounts/login/", json=wrong_login_data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 400:
            print("   ✅ Correctly rejected wrong credentials")
        else:
            print(f"   ❌ Should reject wrong credentials: {response.text}")

    except Exception as e:
        print(f"   ❌ Wrong login test error: {e}")


def main():
    print("🧪 LOGIN ENDPOINT TEST")
    print("=" * 40)

    # Server check
    try:
        response = requests.get(f"{BASE_URL}/common/setting/", timeout=5)
        print("✅ Server is running\n")
    except:
        print("❌ Server is not running! Please start with: python manage.py runserver")
        return

    test_login()

    print("\n🎉 Login test completed!")


if __name__ == '__main__':
    main()
