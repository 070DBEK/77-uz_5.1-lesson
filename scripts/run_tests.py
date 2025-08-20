#!/usr/bin/env python
"""
Barcha testlarni ishga tushirish uchun script
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.test.utils import get_runner
from django.conf import settings


def run_tests():
    """Testlarni ishga tushirish"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    django.setup()
    print("🧪 Running all tests...")

    execute_from_command_line(['manage.py', 'test', '--verbosity=2'])

    print("\n📊 Test coverage report:")
    # Coverage report
    try:
        execute_from_command_line(['coverage', 'run', '--source=.', 'manage.py', 'test'])
        execute_from_command_line(['coverage', 'report'])
        execute_from_command_line(['coverage', 'html'])
        print("📈 HTML coverage report created in htmlcov/")
    except:
        print("⚠️  Coverage not installed. Install with: pip install coverage")


if __name__ == '__main__':
    run_tests()
