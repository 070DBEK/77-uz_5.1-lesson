#!/usr/bin/env python
"""
Tezkor tuzatish - kategoriyalar va test
"""
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


def quick_fix():
    """Tezkor tuzatish"""
    print("🔧 QUICK FIX - Categories & Test")
    print("=" * 40)

    # 1. Load initial data
    print("1️⃣ Loading initial data...")
    try:
        from scripts.load_initial_data import load_initial_data
        load_initial_data()
    except Exception as e:
        print(f"   ❌ Error loading data: {e}")
        return

    # 2. Check categories
    print("\n2️⃣ Checking categories...")
    try:
        from scripts.check_categories import check_categories
        category_id = check_categories()
    except Exception as e:
        print(f"   ❌ Error checking categories: {e}")
        return

    # 3. Test improved flow
    print("\n3️⃣ Testing improved flow...")
    try:
        from scripts.test_improved_flow import test_improved_flow
        test_improved_flow()
    except Exception as e:
        print(f"   ❌ Error testing flow: {e}")
        return

    print("\n🎉 Quick fix completed!")


if __name__ == '__main__':
    quick_fix()
