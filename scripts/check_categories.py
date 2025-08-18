#!/usr/bin/env python
"""
Mavjud kategoriyalarni tekshirish
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

from apps.store.models import Category


def check_categories():
    """Kategoriyalarni tekshirish"""
    print("📂 CHECKING CATEGORIES")
    print("=" * 40)

    categories = Category.objects.all()

    if not categories.exists():
        print("❌ No categories found!")
        print("   Run: python scripts/load_initial_data.py")
        return None

    print(f"✅ Found {categories.count()} categories:")

    for category in categories:
        print(f"   ID: {category.id} - {category.name} (Active: {category.is_active})")

        # Sub-categories
        children = category.children.all()
        if children.exists():
            for child in children:
                print(f"      └── ID: {child.id} - {child.name} (Active: {child.is_active})")

    # Return first active category ID
    first_active = categories.filter(is_active=True).first()
    if first_active:
        print(f"\n🎯 Use category ID: {first_active.id} for testing")
        return first_active.id

    return None


if __name__ == '__main__':
    check_categories()
