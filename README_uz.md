# KirishUshbu - Onlayn Savdo Platformasi

[![English](https://img.shields.io/badge/🇬🇧_English-README.md-green)](README) [![Russian](https://img.shields.io/badge/🇷🇺_Русский-README_ru.md-red)](README_ru.md)

KirishUshbu loyiha — O'zbekiston uchun zamonaviy onlayn savdo platformasi bo'lib, foydalanuvchilarga mahsulotlarni qo'shish, sotish va xarid qilish imkoniyatini beradi.

## 🌟 Asosiy Xususiyatlar

- **🔐 Uch xil rol**: Super Admin, Admin, Sotuvchi
- **🌍 Ikki tilda**: O'zbek (lotin) va Rus tillari
- **📱 To'liq API**: REST API with Swagger hujjatlari
- **🛡️ Xavfsizlik**: JWT autentifikatsiya, CORS, ruxsat nazorati
- **⚙️ Admin Panel**: Django admin interfeysi
- **🧪 Test Coverage**: Keng qamrovli test to'plami

## 🛠️ Texnologiyalar

- **Backend**: Django 4.2, Django REST Framework
- **Ma'lumotlar bazasi**: PostgreSQL / SQLite
- **Autentifikatsiya**: JWT (Simple JWT)
- **Hujjatlar**: drf-spectacular (Swagger)
- **Test**: pytest-django

## 📦 O'rnatish

### 1. Repository'ni clone qiling
\`\`\`bash
git clone <repository-url>
cd kirish-ushbu-backend
\`\`\`

### 2. Virtual environment yarating
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
\`\`\`

### 3. Dependencies o'rnating
\`\`\`bash
pip install -r requirements/development.txt
\`\`\`

### 4. Environment variables sozlang
\`\`\`bash
cp .env.example .env
# .env faylini tahrirlang
\`\`\`

### 5. Ma'lumotlar bazasini sozlang
\`\`\`bash
python scripts/setup_database.py
\`\`\`

### 6. Boshlang'ich ma'lumotlarni yuklang
\`\`\`bash
python scripts/load_initial_data.py
\`\`\`

### 7. Superuser yarating
\`\`\`bash
python scripts/create_superuser.py
\`\`\`

### 8. Serverni ishga tushiring
\`\`\`bash
python manage.py runserver
\`\`\`

## 🚀 Tezkor Boshlash

Barcha qadamlarni bir vaqtda bajarish uchun:
\`\`\`bash
python scripts/quick_fix.py
python manage.py runserver
\`\`\`

## 📚 API Hujjatlari

API hujjatlari Swagger UI orqali mavjud:
- **Development**: http://localhost:8000/swagger/
- **API Schema**: http://localhost:8000/api/schema/
- **Admin Panel**: http://localhost:8000/default-admin-panel/

### Asosiy Endpoint'lar

#### 👤 Accounts (Hisoblar)
- `POST /api/v1/accounts/register/` - Ro'yxatdan o'tish
- `POST /api/v1/accounts/login/` - Tizimga kirish
- `GET /api/v1/accounts/me/` - Profil ma'lumotlari
- `PUT /api/v1/accounts/edit/` - Profilni tahrirlash
- `POST /api/v1/accounts/seller/registration/` - Sotuvchi bo'lish uchun ariza

#### 🏪 Store (Do'kon)
- `GET /api/v1/store/category/` - Kategoriyalar ro'yxati
- `POST /api/v1/store/ads/` - E'lon yaratish
- `GET /api/v1/store/list/ads/` - E'lonlar ro'yxati
- `GET /api/v1/store/my-ads/` - Mening e'lonlarim

#### 🌍 Common (Umumiy)
- `GET /api/v1/common/regions-with-districts/` - Viloyat va tumanlar
- `GET /api/v1/common/pages/` - Statik sahifalar
- `GET /api/v1/common/setting/` - Ilova sozlamalari

## 🔐 Rollar va Ruxsatlar

### 👑 Super Admin
- Barcha modullarga to'liq kirish
- Loyiha ustidan to'liq nazorat
- Admin user yaratish
- Barcha user'larni ko'rish va boshqarish

### 🛡️ Admin
- Sotuvchilarni qo'shish va boshqarish
- Seller registration'larni approve/reject qilish
- User'larni ko'rish (super admin'dan tashqari)

### 🏪 Seller (Sotuvchi)
- Faqat o'z mahsulotlarini qo'shish
- Faqat o'z mahsulotlarini tahrirlash
- O'z profil ma'lumotlarini tahrirlash

## 🧪 Test

Testlarni ishga tushirish:
\`\`\`bash
pytest
\`\`\`

Coverage hisoboti:
\`\`\`bash
pytest --cov=apps --cov-report=html
\`\`\`

Rol-based testlar:
\`\`\`bash
python scripts/test_role_permissions.py
\`\`\`

## 📁 Loyiha Tuzilishi

\`\`\`
kirish-ushbu-backend/
├── apps/
│   ├── accounts/          # Foydalanuvchi boshqaruvi
│   ├── store/            # Mahsulotlar, kategoriyalar, e'lonlar
│   └── common/           # Umumiy yordamchi modullar
├── config/               # Django sozlamalari
├── requirements/         # Dependencies
├── scripts/             # Ma'lumotlar bazasi skriptlari
├── tests/               # Test fayllari
└── manage.py
\`\`\`

## 🌍 Ikki Til Qo'llab-quvvatlash

Tizim quyidagi tillarda ishlaydi:
- **O'zbek tili** (lotin yozuvi) - `_uz` field'lar
- **Rus tili** - `_ru` field'lar

### Model Misoli:
\`\`\`python
class Ad(models.Model):
    name_uz = models.CharField(max_length=255)  # O'zbek nomi
    name_ru = models.CharField(max_length=255)  # Rus nomi
    description_uz = models.TextField()         # O'zbek tavsifi
    description_ru = models.TextField()         # Rus tavsifi
\`\`\`

## 🚀 Production'ga Deploy

1. Environment o'zgaruvchilarini sozlang:
\`\`\`bash
export DJANGO_SETTINGS_MODULE=config.settings.production
\`\`\`

2. Static fayllarni to'plang:
\`\`\`bash
python manage.py collectstatic
\`\`\`

3. Gunicorn yoki uWSGI ishlatib deploy qiling:
\`\`\`bash
gunicorn config.wsgi:application
\`\`\`

## 📊 Ma'lumotlar Bazasi

### Development uchun SQLite
\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
\`\`\`

### Production uchun PostgreSQL
\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kirish_ushbu',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
\`\`\`

## 🔧 Foydali Skriptlar

- `scripts/setup_database.py` - Ma'lumotlar bazasini sozlash
- `scripts/load_initial_data.py` - Boshlang'ich ma'lumotlarni yuklash
- `scripts/create_superuser.py` - Super admin yaratish
- `scripts/check_categories.py` - Kategoriyalarni tekshirish
- `scripts/test_role_permissions.py` - Ruxsatlarni test qilish

## 🤝 Hissa Qo'shish

1. Repository'ni fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Branch'ni push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

## 📞 Qo'llab-quvvatlash

- **Email**: info@uic.group
- **Telefon**: +998 71 234 56 78
- **Telegram**: @support_77uz

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun [LICENSE](LICENSE) faylini ko'ring.

---

**© 2025 KirishUshbu Platform. Barcha huquqlar himoyalangan.**
