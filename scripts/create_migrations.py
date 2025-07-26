#!/usr/bin/env python
"""
Migration yaratish uchun script
"""
import os
import sys
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    django.setup()

    from django.core.management import execute_from_command_line

    # Migrations yaratish
    execute_from_command_line(['manage.py', 'makemigrations', 'accounts'])
    execute_from_command_line(['manage.py', 'makemigrations', 'common'])
    execute_from_command_line(['manage.py', 'makemigrations', 'store'])

    print("Migrations created successfully!")
