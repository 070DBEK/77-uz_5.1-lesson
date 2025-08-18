#!/usr/bin/env python
"""
Login muammosini debug qilish
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def debug_login():
    """Login debug qilish"""
    print("🔍 DEBUGGING LOGIN ISSUE")
    print("=" * 40)

    # 1. Server status check
    try:
        response = requests.get(f"{BASE_URL}/common/setting/")
        print(f"✅ Server running - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return

    # 2. Register a test user first
    register_data = {
        "full_name": "Debug User",
        "phone_number": "+998901111111",
        "password": "debug123",
        "password_confirm": "debug123",
        "role": "customer"
    }

    print("\n1️⃣ Registering test user...")
    try:
        response = requests.post(f"{BASE_URL}/accounts/register/", json=register_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ User registered")
        elif response.status_code == 400:
            print("   ⚠️ User already exists")
        else:
            print(f"   ❌ Registration failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Registration error: {e}")

    # 3. Test login with detailed debugging
    login_data = {
        "phone_number": "+998901111111",
        "password": "debug123"
    }

    print("\n2️⃣ Testing login with debug info...")
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post(
            f"{BASE_URL}/accounts/login/",
            json=login_data,
            headers=headers
        )

        print(f"   Request URL: {response.url}")
        print(f"   Request Headers: {headers}")
        print(f"   Request Data: {login_data}")
        print(f"   Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("   ✅ Login successful!")
            data = response.json()
            print(f"   🔑 Got access token: {data.get('access_token', 'None')[:50]}...")
        else:
            print(f"   ❌ Login failed")
            print(f"   Response Text: {response.text}")

            # Try to parse JSON error
            try:
                error_data = response.json()
                print(f"   Error Details: {json.dumps(error_data, indent=2)}")
            except:
                print("   Could not parse error as JSON")

    except Exception as e:
        print(f"   ❌ Login request error: {e}")

    # 4. Test with wrong credentials
    print("\n3️⃣ Testing with wrong credentials...")
    wrong_data = {
        "phone_number": "+998901111111",
        "password": "wrongpassword"
    }

    try:
        response = requests.post(f"{BASE_URL}/accounts/login/", json=wrong_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Correctly rejected wrong credentials")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Wrong credentials test error: {e}")


if __name__ == '__main__':
    debug_login()
