# 🛒 77.uz - E-commerce Platform Backend

**77.uz** - O'zbekistondagi eng yirik onlayn bozor platformasi uchun Django REST API backend tizimi.

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)

## 📋 Mundarija

- [Loyiha haqida](#-loyiha-haqida)
- [Texnologiyalar](#-texnologiyalar)
- [O'rnatish](#-ornatish)
- [API Hujjatlari](#-api-hujjatlari)
- [Loyiha strukturasi](#-loyiha-strukturasi)
- [Foydalanuvchi rollari](#-foydalanuvchi-rollari)
- [Ma'lumotlar bazasi](#-malumotlar-bazasi)
- [Deployment](#-deployment)
- [Hissa qo'shish](#-hissa-qoshish)

## 🎯 Loyiha haqida

77.uz platformasi - bu O'zbekiston bozorida faol ishlaydigan e-commerce tizimi bo'lib, quyidagi imkoniyatlarni taqdim etadi:

- 🔐 **Autentifikatsiya** - JWT token asosida xavfsiz kirish tizimi
- 👥 **Foydalanuvchi boshqaruvi** - Customer, Seller, Admin, Super Admin rollari
- 🛍️ **Mahsulot boshqaruvi** - E'lonlar yaratish, tahrirlash va boshqarish
- 📂 **Kategoriyalar** - Ierarxik kategoriya tizimi
- ❤️ **Sevimlilar** - Mahsulotlarni sevimlilar ro'yxatiga qo'shish
- 🔍 **Qidiruv** - Kuchli qidiruv va filtrlash tizimi
- 🌍 **Ko'p tillilik** - O'zbek va Rus tillari qo'llab-quvvatlanadi

## 🚀 Texnologiyalar

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - API development
- **JWT Authentication** - Xavfsiz autentifikatsiya
- **PostgreSQL** - Production database
- **SQLite** - Development database

### Qo'shimcha kutubxonalar
- **django-cors-headers** - CORS boshqaruvi
- **django-filter** - API filtrlash
- **drf-spectacular** - API hujjatlari
- **Pillow** - Rasm bilan ishlash
- **python-decouple** - Environment variables

## 📦 O'rnatish

### 1. Repository'ni klonlash

\`\`\`bash
git clone https://github.com/070DBEK/77-uz_5.1-lesson.git
cd 77uz-backend
\`\`\`

### 2. Virtual environment yaratish

\`\`\`bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Dependencies o'rnatish

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Environment variables sozlash

\`.env\` faylini yarating va quyidagi ma'lumotlarni kiriting:

\`\`\`env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL uchun)
DB_NAME=kirish_ushbu
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
\`\`\`

### 5. Ma'lumotlar bazasini sozlash

\`\`\`bash
# Migratsiyalar yaratish
python manage.py makemigrations

# Migratsiyalarni qo'llash
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser
\`\`\`

### 6. Boshlang'ich ma'lumotlarni yuklash

\`\`\`bash
# Python script orqali
python scripts/load_initial_data.py

# Yoki SQL script orqali
python manage.py dbshell < scripts/initial_data.sql
\`\`\`

### 7. Serverni ishga tushirish

\`\`\`bash
python manage.py runserver
\`\`\`

Server \`http://127.0.0.1:8000\` manzilida ishga tushadi.

## 📚 API Hujjatlari

### Swagger UI
- **URL**: \`http://127.0.0.1:8000/swagger/\`
- **Interaktiv API hujjatlari**

### ReDoc
- **URL**: \`http://127.0.0.1:8000/redoc/\`
- **Batafsil API hujjatlari**

### Admin Panel
- **URL**: \`http://127.0.0.1:8000/default-admin-panel/\`
- **Ma'lumotlar bazasini boshqarish**

## 🏗️ Loyiha strukturasi

\`\`\`
77uz-backend/
├── 📁 apps/                    # Django applications
│   ├── 📁 accounts/            # Foydalanuvchi boshqaruvi
│   │   ├── models.py           # User, Address, SellerRegistration
│   │   ├── views.py            # API views
│   │   ├── serializers.py      # DRF serializers
│   │   ├── permissions.py      # Custom permissions
│   │   └── urls.py             # URL routing
│   ├── 📁 store/               # E-commerce logic
│   │   ├── models.py           # Ad, Category, FavouriteProduct
│   │   ├── views.py            # Store API views
│   │   ├── serializers.py      # Store serializers
│   │   ├── filters.py          # Django filters
│   │   └── urls.py             # Store URLs
│   └── 📁 common/              # Umumiy ma'lumotlar
│       ├── models.py           # Region, District, StaticPage
│       ├── views.py            # Common views
│       └── serializers.py      # Common serializers
├── 📁 config/                  # Django sozlamalari
│   ├── 📁 settings/            # Environment-specific settings
│   │   ├── base.py             # Asosiy sozlamalar
│   │   ├── development.py      # Development sozlamalari
│   │   └── production.py       # Production sozlamalari
│   ├── urls.py                 # Asosiy URL routing
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── 📁 scripts/                 # Utility scripts
│   ├── load_initial_data.py    # Boshlang'ich ma'lumotlar
│   ├── initial_data.sql        # SQL ma'lumotlar
│   └── fix_initial_data.sql    # Ma'lumotlarni tuzatish
├── 📄 requirements.txt         # Python dependencies
├── 📄 manage.py               # Django management
├── 📄 .env                    # Environment variables
├── 📄 .gitignore              # Git ignore rules
└── 📄 README.md               # Loyiha hujjatlari
\`\`\`

## 👥 Foydalanuvchi rollari

### 🔴 Super Admin
- Barcha tizim huquqlari
- Admin foydalanuvchilarni yaratish
- Barcha ma'lumotlarga kirish

### 🟠 Admin
- Sotuvchilarni boshqarish
- E'lonlarni tasdiqlash/rad etish
- Foydalanuvchilarni boshqarish

### 🟡 Seller
- O'z e'lonlarini yaratish va boshqarish
- Mahsulot rasmlarini yuklash
- Statistikalarni ko'rish

### 🟢 Customer
- E'lonlarni ko'rish va qidirish
- Sevimlilar ro'yxati
- Seller bo'lish uchun ariza berish

## 🗄️ Ma'lumotlar bazasi

### Asosiy jadvallar

- **users** - Foydalanuvchilar ma'lumotlari
- **addresses** - Foydalanuvchi manzillari
- **seller_registrations** - Seller bo'lish arizalari
- **categories** - Mahsulot kategoriyalari
- **ads** - E'lonlar
- **ad_photos** - E'lon rasmlari
- **favourite_products** - Sevimli mahsulotlar
- **regions** - Viloyatlar
- **districts** - Tumanlar
- **static_pages** - Statik sahifalar

## 🚀 Deployment

### Production uchun sozlash

1. **Environment variables**:
\`\`\`env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=strong_password
\`\`\`

2. **Static files**:
\`\`\`bash
python manage.py collectstatic
\`\`\`

3. **Database migration**:
\`\`\`bash
python manage.py migrate --settings=config.settings.production
\`\`\`

### Docker bilan ishga tushirish

\`\`\`dockerfile
# Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
\`\`\`

\`\`\`bash
# Docker build va run
docker build -t 77uz-backend .
docker run -p 8000:8000 77uz-backend
\`\`\`

## 🤝 Hissa qo'shish

1. **Fork** qiling
2. **Feature branch** yarating (\`git checkout -b feature/AmazingFeature\`)
3. **Commit** qiling (\`git commit -m 'Add some AmazingFeature'\`)
4. **Push** qiling (\`git push origin feature/AmazingFeature\`)
5. **Pull Request** oching

### Code Style

- **PEP 8** standartlariga rioya qiling
- **Black** formatter ishlatiladi
- **Type hints** qo'shing
- **Docstring**lar yozing

## 📞 Aloqa

- **Email**: info@uic.group
- **Telegram**: @your_username
- **Website**: https://77.uz

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun [LICENSE](LICENSE) faylini ko'ring.

---

**77.uz Backend API** - O'zbekiston e-commerce platformasi 🇺🇿
\`\`\`

Bu README.md fayli loyihangiz uchun to'liq va professional ko'rinishga ega. Unda barcha kerakli ma'lumotlar, o'rnatish yo'riqnomalari va loyiha strukturasi batafsil yoritilgan.
\`\`\`
