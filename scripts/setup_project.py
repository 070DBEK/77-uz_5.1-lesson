#!/usr/bin/env python
"""
Loyihani sozlash uchun script
"""
import os
import sys
import django
from pathlib import Path


def setup_project():
    """Loyihani to'liq sozlash"""

    # Base directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # 1. Kerakli papkalarni yaratish
    folders_to_create = [
        'static',
        'media',
        'media/profiles',
        'media/ads',
        'media/icons',
        'media/search_icons',
        'logs',
    ]

    for folder in folders_to_create:
        folder_path = BASE_DIR / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created folder: {folder}")

    # 2. .env fayl yaratish (agar mavjud bo'lmasa)
    env_file = BASE_DIR / '.env'
    if not env_file.exists():
        env_content = """# Database (SQLite uchun kerak emas)
DB_NAME=kirish_ushbu
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Redis
REDIS_URL=redis://localhost:6379/0
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")

    print("\n🎉 Project setup completed!")
    print("\nNext steps:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
    print("4. python manage.py runserver")


if __name__ == '__main__':
    setup_project()

