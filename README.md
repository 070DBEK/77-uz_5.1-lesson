# KirishUshbu - Online Marketplace Platform

🌐 **Choose your language / Tilni tanlang / Выберите язык:**

[![Uzbek](https://img.shields.io/badge/🇺🇿_O'zbek-README_uz.md-blue)](README_uz.md)
[![Russian](https://img.shields.io/badge/🇷🇺_Русский-README_ru.md-red)](README_ru.md)

---

## Quick Start / Tezkor boshlash / Быстрый старт

\`\`\`bash
# Clone repository
git clone <repository-url>
cd kirish-ushbu-backend

# Setup environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements/development.txt

# Setup database and run
python scripts/quick_fix.py
python manage.py runserver
\`\`\`

## Xususiyatlar

- **Uch xil rol**: Super Admin, Admin, Sotuvchi
- **To'liq API**: REST API with Swagger documentation
- **Xavfsizlik**: JWT authentication, CORS, permission controls
- **Admin Panel**: Django admin interface
- **Test Coverage**: Comprehensive test suite

## 🌍 Language Support / Til qo'llab-quvvatlash / Языковая поддержка

This system supports two languages:
- **Uzbek** (Latin script) - O'zbek tili (lotin yozuvi)
- **Russian** - Русский язык

## Texnologiyalar

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Documentation**: drf-spectacular (Swagger)
- **Testing**: pytest-django

## 📚 Documentation / Hujjatlar / Документация

- [🇺🇿 O'zbek tilida to'liq hujjat](README_uz.md)
- [🇷🇺 Полная документация на русском](README_ru.md)

## O'rnatish

1. **Repository'ni clone qiling**:
\`\`\`bash
git clone <repository-url>
cd kirish-ushbu-backend
\`\`\`

2. **Virtual environment yarating**:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
\`\`\`

3. **Dependencies o'rnating**:
\`\`\`bash
pip install -r requirements/development.txt
\`\`\`

4. **Environment variables sozlang**:
\`\`\`bash
cp .env.example .env
# .env faylini tahrirlang
\`\`\`

5. **Database yarating va migrate qiling**:
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

6. **Initial data yuklang**:
\`\`\`bash
python manage.py shell < scripts/initial_data.sql
\`\`\`

7. **Superuser yarating**:
\`\`\`bash
python manage.py createsuperuser
\`\`\`

8. **Serverni ishga tushiring**:
\`\`\`bash
python manage.py runserver
\`\`\`

## 🚀 API Documentation

- **Swagger UI**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/default-admin-panel/

## API Endpoints

### Accounts
- `POST /api/v1/accounts/register/` - Ro'yxatdan o'tish
- `POST /api/v1/accounts/login/` - Kirish
- `GET /api/v1/accounts/me/` - Profil ma'lumotlari
- `PUT /api/v1/accounts/edit/` - Profilni tahrirlash

### Store
- `GET /api/v1/store/category/` - Kategoriyalar ro'yxati
- `POST /api/v1/store/ads/` - E'lon yaratish
- `GET /api/v1/store/list/ads/` - E'lonlar ro'yxati
- `GET /api/v1/store/my-ads/` - Mening e'lonlarim

### Common
- `GET /api/v1/common/regions-with-districts/` - Viloyat va tumanlar
- `GET /api/v1/common/pages/` - Statik sahifalar
- `GET /api/v1/common/setting/` - Ilova sozlamalari

## Deployment

Production uchun:
1. `DJANGO_SETTINGS_MODULE=config.settings.production` o'rnating
2. Static fayllarni to'plang: `python manage.py collectstatic`
3. Gunicorn yoki uWSGI ishlatib deploy qiling

## 📞 Support / Qo'llab-quvvatlash / Поддержка

- **Email**: info@uic.group
- **Phone**: +998 71 234 56 78

## Contributing

1. Fork qiling
2. Feature branch yarating
3. Testlar yozing
4. Pull request yuboring

## License

MIT License

---

**© 2025 KirishUshbu Platform. All rights reserved.**
