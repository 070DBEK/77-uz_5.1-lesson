#!/usr/bin/env python
"""
Barcha setup qadamlarini bir vaqtda bajarish
"""
import os
import sys
import subprocess


def run_command(command, description):
    """Command ishga tushirish"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        return False


def run_all_setup():
    """Barcha setup qadamlarini bajarish"""
    print("🚀 Starting Complete Setup...")

    # 1. Database setup
    if not run_command("python scripts/setup_database.py", "Setting up database"):
        return

    # 2. Load initial data
    if not run_command("python scripts/load_initial_data.py", "Loading initial data"):
        return

    # 3. Create superuser
    print("\n👤 Creating superuser...")
    print("Default values will be used:")
    print("Phone: +998901234567")
    print("Name: Super Admin")
    print("Password: admin123")

    if not run_command("python scripts/create_superuser.py", "Creating superuser"):
        return

    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. python manage.py runserver")
    print("2. Open http://localhost:8000/swagger/")
    print("3. Admin: http://localhost:8000/default-admin-panel/")
    print("   Login: +998901234567 / admin123")


if __name__ == '__main__':
    run_all_setup()
