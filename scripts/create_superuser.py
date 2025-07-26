#!/usr/bin/env python
"""
Super admin yaratish uchun script
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """Super admin yaratish"""

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

    user = User.objects.create_user(
        phone_number=phone_number,
        full_name=full_name,
        password=password,
        role='super_admin'
    )

    print(f"✅ Super admin created successfully!")
    print(f"Phone: {phone_number}")
    print(f"Password: {password}")
    print(f"Role: {user.role}")
    print(f"Admin panel: http://localhost:8000/default-admin-panel/")

if __name__ == '__main__':
    create_superuser()
