#!/usr/bin/env python
"""
Super admin yaratish uchun script - to'g'rilangan versiya
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

User = get_user_model()


def create_superuser():
    """Super admin yaratish"""

    print("👤 Creating Super Admin User...")

    phone_number = input("Phone number (+998901234567): ").strip()
    if not phone_number:
        phone_number = "+998901234567"

    full_name = input("Full name (Super Admin): ").strip()
    if not full_name:
        full_name = "Super Admin"

    password = input("Password (admin123): ").strip()
    if not password:
        password = "admin123"

    # Super admin yaratish
    if User.objects.filter(phone_number=phone_number).exists():
        print(f"❌ User with phone {phone_number} already exists!")
        return

    try:
        # Custom User model uchun to'g'ri create_user metodi
        user = User.objects.create(
            phone_number=phone_number,
            full_name=full_name,
            role='super_admin',
            is_staff=True,
            is_superuser=True
        )
        user.set_password(password)
        user.save()

        print(f"\n✅ Super admin created successfully!")
        print(f"📱 Phone: {phone_number}")
        print(f"🔑 Password: {password}")
        print(f"👑 Role: {user.role}")
        print(f"🌐 Admin panel: http://localhost:8000/default-admin-panel/")
        print(f"📚 API docs: http://localhost:8000/swagger/")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        print("\nAlternative method: Use Django management command:")
        print("python manage.py createsuperuser")


if __name__ == '__main__':
    create_superuser()
