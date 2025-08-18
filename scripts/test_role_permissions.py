#!/usr/bin/env python
"""
Har bir rol uchun permission'larni amaliy test qilish
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

from django.contrib.auth import get_user_model
from apps.store.models import Category, Ad

User = get_user_model()


def create_test_users():
    """Test uchun user'lar yaratish"""
    print("👥 Creating test users...")

    # Super Admin
    super_admin, created = User.objects.get_or_create(
        phone_number="+998900000001",
        defaults={
            'full_name': 'Test Super Admin',
            'role': 'super_admin'
        }
    )
    if created:
        super_admin.set_password('test123')
        super_admin.save()
        print("✅ Super Admin created")

    # Admin
    admin, created = User.objects.get_or_create(
        phone_number="+998900000002",
        defaults={
            'full_name': 'Test Admin',
            'role': 'admin'
        }
    )
    if created:
        admin.set_password('test123')
        admin.save()
        print("✅ Admin created")

    # Seller
    seller, created = User.objects.get_or_create(
        phone_number="+998900000003",
        defaults={
            'full_name': 'Test Seller',
            'role': 'seller'
        }
    )
    if created:
        seller.set_password('test123')
        seller.save()
        print("✅ Seller created")

    return super_admin, admin, seller


def test_user_properties():
    """User properties test qilish"""
    print("\n🔍 Testing user properties...")

    super_admin, admin, seller = create_test_users()

    # Super Admin properties
    print(f"\n👑 Super Admin ({super_admin.phone_number}):")
    print(f"   is_staff: {super_admin.is_staff}")
    print(f"   is_superuser: {super_admin.is_superuser}")
    print(f"   is_super_admin: {super_admin.is_super_admin}")
    print(f"   is_admin_user: {super_admin.is_admin_user}")

    # Admin properties
    print(f"\n🛡️  Admin ({admin.phone_number}):")
    print(f"   is_staff: {admin.is_staff}")
    print(f"   is_superuser: {admin.is_superuser}")
    print(f"   is_super_admin: {admin.is_super_admin}")
    print(f"   is_admin_user: {admin.is_admin_user}")

    # Seller properties
    print(f"\n🏪 Seller ({seller.phone_number}):")
    print(f"   is_staff: {seller.is_staff}")
    print(f"   is_superuser: {seller.is_superuser}")
    print(f"   is_super_admin: {seller.is_super_admin}")
    print(f"   is_seller_user: {seller.is_seller_user}")


def test_queryset_permissions():
    """Queryset permissions test qilish"""
    print("\n📊 Testing queryset permissions...")

    super_admin, admin, seller = create_test_users()

    # Super Admin - barcha user'larni ko'ra oladi
    if super_admin.role == 'super_admin':
        all_users = User.objects.all()
        print(f"👑 Super Admin ko'radigan user'lar: {all_users.count()}")

    # Admin - super admin'dan tashqari barcha user'larni ko'ra oladi
    if admin.role == 'admin':
        admin_visible_users = User.objects.exclude(role='super_admin')
        print(f"🛡️  Admin ko'radigan user'lar: {admin_visible_users.count()}")

    # Seller - faqat o'z ad'larini ko'ra oladi
    seller_ads = Ad.objects.filter(seller=seller)
    print(f"🏪 Seller ko'radigan ad'lar: {seller_ads.count()}")


def main():
    """Asosiy test funksiyasi"""
    print("🧪 ROLE PERMISSIONS TEST")
    print("=" * 50)

    test_user_properties()
    test_queryset_permissions()

    print("\n✅ Permission tests completed!")


if __name__ == '__main__':
    main()
