#!/usr/bin/env python
"""
Database sozlash uchun script
"""
import os
import sys
import subprocess
import django

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')


def run_command(command, description):
    """Command ishga tushirish"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def setup_database():
    """Database sozlash"""
    print("🚀 Database Setup Starting...")

    # 1. Migrations
    if not run_command("python manage.py makemigrations accounts", "Creating accounts migrations"):
        return

    if not run_command("python manage.py makemigrations common", "Creating common migrations"):
        return

    if not run_command("python manage.py makemigrations store", "Creating store migrations"):
        return

    if not run_command("python manage.py migrate", "Applying migrations"):
        return

    print("\n🎉 Database setup completed!")
    print("\n📋 Next steps:")
    print("1. python scripts/load_initial_data.py")
    print("2. python scripts/create_superuser.py")
    print("3. python manage.py runserver")


if __name__ == '__main__':
    setup_database()
