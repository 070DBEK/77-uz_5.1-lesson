#!/usr/bin/env python
"""
Initial data yuklash uchun Python script - yangilangan versiya
"""
import os
import sys
import django
from pathlib import Path

# Loyiha root direktoriyasini aniqlash
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.common.models import Region, District, StaticPage, Setting
from apps.store.models import Category, PopularSearchTerm


def load_initial_data():
    """Initial data yuklash"""

    print("📊 Loading initial data...")

    # 1. Regions
    regions_data = [
        'Toshkent shahar / г. Ташкент',
        'Andijon viloyati / Андижанская область',
        'Buxoro viloyati / Бухарская область',
        'Farg\'ona viloyati / Ферганская область',
        'Jizzax viloyati / Джизакская область',
        'Xorazm viloyati / Хорезмская область',
        'Namangan viloyati / Наманганская область',
        'Navoiy viloyati / Навоийская область',
        'Qashqadaryo viloyati / Кашкадарьинская область',
        'Qoraqalpog\'iston Respublikasi / Республика Каракалпакстан',
        'Samarqand viloyati / Самаркандская область',
        'Sirdaryo viloyati / Сырдарьинская область',
        'Surxondaryo viloyati / Сурхандарьинская область',
        'Toshkent viloyati / Ташкентская область',
    ]

    for region_name in regions_data:
        region, created = Region.objects.get_or_create(name=region_name)
        if created:
            print(f"✅ Created region: {region_name}")

    # 2. Districts for Tashkent
    tashkent = Region.objects.filter(name__contains='Toshkent shahar').first()
    if tashkent:
        districts_data = [
            'Chilonzor tumani / Чиланзарский район',
            'Mirobod tumani / Мирабадский район',
            'Yunusobod tumani / Юнусабадский район',
            'Shayxontohur tumani / Шайхантахурский район',
            'Olmazor tumani / Алмазарский район',
            'Bektemir tumani / Бектемирский район',
            'Uchtepa tumani / Учтепинский район',
            'Yakkasaray tumani / Яккасарайский район',
            'Yashnobod tumani / Яшнабадский район',
            'Sergeli tumani / Сергелийский район',
        ]

        for district_name in districts_data:
            district, created = District.objects.get_or_create(
                region=tashkent,
                name=district_name
            )
            if created:
                print(f"✅ Created district: {district_name}")

    # 3. Categories (MUHIM!)
    categories_data = [
        'Elektronika / Электроника',
        'Kiyim-kechak / Одежда',
        'Uy-ro\'zg\'or buyumlari / Товары для дома',
        'Sport va dam olish / Спорт и отдых',
        'Avtomobillar / Автомобили',
        'Ko\'chmas mulk / Недвижимость',
        'Xizmatlar / Услуги',
    ]

    created_categories = []
    for category_name in categories_data:
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'is_active': True}
        )
        if created:
            print(f"✅ Created category: {category_name}")
        created_categories.append(category)

    # 4. Subcategories for Electronics
    electronics = Category.objects.filter(name__contains='Elektronika').first()
    if electronics:
        subcategories_data = [
            'Telefonlar / Телефоны',
            'Noutbuklar / Ноутбуки',
            'Televizorlar / Телевизоры',
            'Muzlatgichlar / Холодильники',
            'Kir yuvish mashinalari / Стиральные машины',
        ]

        for subcategory_name in subcategories_data:
            subcategory, created = Category.objects.get_or_create(
                name=subcategory_name,
                parent=electronics,
                defaults={'is_active': True}
            )
            if created:
                print(f"✅ Created subcategory: {subcategory_name}")

    # 5. Static Pages
    pages_data = [
        {
            'slug': 'about-us',
            'title': 'Biz haqimizda / О нас',
            'content': '77.uz - O\'zbekistondagi eng yirik onlayn bozor. Мы крупнейший онлайн-рынок в Узбекистане.'
        },
        {
            'slug': 'privacy-policy',
            'title': 'Maxfiylik siyosati / Политика конфиденциальности',
            'content': 'Maxfiylik siyosati matni...'
        },
        {
            'slug': 'terms-of-service',
            'title': 'Foydalanish shartlari / Условия использования',
            'content': 'Foydalanish shartlari matni...'
        }
    ]

    for page_data in pages_data:
        page, created = StaticPage.objects.get_or_create(
            slug=page_data['slug'],
            defaults={
                'title': page_data['title'],
                'content': page_data['content']
            }
        )
        if created:
            print(f"✅ Created page: {page_data['title']}")

    # 6. Settings
    setting, created = Setting.objects.get_or_create(
        id=1,
        defaults={
            'phone': '+998712345678',
            'support_email': 'support@77.uz',
            'working_hours': 'Dushanba-Yakshanba 9:00-21:00 / Пн-Вс 9:00-21:00',
            'app_version': '1.0.0',
            'maintenance_mode': False
        }
    )
    if created:
        print("✅ Created application settings")

    # 7. Popular Search Terms
    search_terms_data = [
        {'name': 'iPhone / Айфон', 'search_count': 15234},
        {'name': 'Samsung Galaxy / Самсунг Галакси', 'search_count': 12456},
        {'name': 'Noutbuk / Ноутбук', 'search_count': 9876},
        {'name': 'Kiyim / Одежда', 'search_count': 8765},
        {'name': 'Avtomobil / Автомобиль', 'search_count': 7654},
    ]

    for term_data in search_terms_data:
        term, created = PopularSearchTerm.objects.get_or_create(
            name=term_data['name'],
            defaults={'search_count': term_data['search_count']}
        )
        if created:
            print(f"✅ Created search term: {term_data['name']}")

    print("\n🎉 Initial data loaded successfully!")
    print(f"📊 Statistics:")
    print(f"   - Regions: {Region.objects.count()}")
    print(f"   - Districts: {District.objects.count()}")
    print(f"   - Categories: {Category.objects.count()}")
    print(f"   - Static Pages: {StaticPage.objects.count()}")
    print(f"   - Search Terms: {PopularSearchTerm.objects.count()}")

    # Show available category IDs
    print(f"\n📂 Available Categories:")
    categories = Category.objects.filter(is_active=True)
    for cat in categories:
        print(f"   ID: {cat.id} - {cat.name}")


if __name__ == '__main__':
    load_initial_data()
