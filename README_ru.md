# KirishUshbu - Платформа Онлайн Торговли

[![English](https://img.shields.io/badge/🇬🇧_English-README.md-green)](README) [![O'zbek](https://img.shields.io/badge/🇺🇿_O'zbek-README_uz.md-blue)](README_uz.md)

KirishUshbu — современная платформа онлайн торговли для Узбекистана, предоставляющая пользователям возможность добавлять, продавать и покупать товары.

## 🌟 Основные Особенности

- **🔐 Три роли**: Супер Админ, Админ, Продавец
- **🌍 Два языка**: Узбекский (латиница) и Русский
- **📱 Полный API**: REST API с документацией Swagger
- **🛡️ Безопасность**: JWT аутентификация, CORS, контроль разрешений
- **⚙️ Админ Панель**: Интерфейс Django admin
- **🧪 Покрытие Тестами**: Комплексный набор тестов

## 🛠️ Технологии

- **Backend**: Django 4.2, Django REST Framework
- **База данных**: PostgreSQL / SQLite
- **Аутентификация**: JWT (Simple JWT)
- **Документация**: drf-spectacular (Swagger)
- **Тестирование**: pytest-django

## 📦 Установка

### 1. Клонируйте репозиторий
\`\`\`bash
git clone <repository-url>
cd kirish-ushbu-backend
\`\`\`

### 2. Создайте виртуальное окружение
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
\`\`\`

### 3. Установите зависимости
\`\`\`bash
pip install -r requirements/development.txt
\`\`\`

### 4. Настройте переменные окружения
\`\`\`bash
cp .env.example .env
# Отредактируйте файл .env
\`\`\`

### 5. Настройте базу данных
\`\`\`bash
python scripts/setup_database.py
\`\`\`

### 6. Загрузите начальные данные
\`\`\`bash
python scripts/load_initial_data.py
\`\`\`

### 7. Создайте суперпользователя
\`\`\`bash
python scripts/create_superuser.py
\`\`\`

### 8. Запустите сервер
\`\`\`bash
python manage.py runserver
\`\`\`

## 🚀 Быстрый Старт

Для выполнения всех шагов одновременно:
\`\`\`bash
python scripts/quick_fix.py
python manage.py runserver
\`\`\`

## 📚 Документация API

Документация API доступна через Swagger UI:
- **Development**: http://localhost:8000/swagger/
- **API Schema**: http://localhost:8000/api/schema/
- **Админ Панель**: http://localhost:8000/default-admin-panel/

### Основные Endpoint'ы

#### 👤 Accounts (Аккаунты)
- `POST /api/v1/accounts/register/` - Регистрация
- `POST /api/v1/accounts/login/` - Вход в систему
- `GET /api/v1/accounts/me/` - Данные профиля
- `PUT /api/v1/accounts/edit/` - Редактирование профиля
- `POST /api/v1/accounts/seller/registration/` - Заявка на становление продавцом

#### 🏪 Store (Магазин)
- `GET /api/v1/store/category/` - Список категорий
- `POST /api/v1/store/ads/` - Создание объявления
- `GET /api/v1/store/list/ads/` - Список объявлений
- `GET /api/v1/store/my-ads/` - Мои объявления

#### 🌍 Common (Общие)
- `GET /api/v1/common/regions-with-districts/` - Области и районы
- `GET /api/v1/common/pages/` - Статические страницы
- `GET /api/v1/common/setting/` - Настройки приложения

## 🔐 Роли и Разрешения

### 👑 Супер Админ
- Полный доступ ко всем модулям
- Полный контроль над проектом
- Создание админ пользователей
- Просмотр и управление всеми пользователями

### 🛡️ Админ
- Добавление и управление продавцами
- Одобрение/отклонение заявок продавцов
- Просмотр пользователей (кроме супер админов)

### 🏪 Продавец
- Добавление только своих товаров
- Редактирование только своих товаров
- Редактирование данных своего профиля

## 🧪 Тестирование

Запуск тестов:
\`\`\`bash
pytest
\`\`\`

Отчет о покрытии:
\`\`\`bash
pytest --cov=apps --cov-report=html
\`\`\`

Тесты на основе ролей:
\`\`\`bash
python scripts/test_role_permissions.py
\`\`\`

## 📁 Структура Проекта

\`\`\`
kirish-ushbu-backend/
├── apps/
│   ├── accounts/          # Управление пользователями
│   ├── store/            # Товары, категории, объявления
│   └── common/           # Общие вспомогательные модули
├── config/               # Настройки Django
├── requirements/         # Зависимости
├── scripts/             # Скрипты базы данных
├── tests/               # Тестовые файлы
└── manage.py
\`\`\`

## 🌍 Поддержка Двух Языков

Система работает на следующих языках:
- **Узбекский язык** (латиница) - поля `_uz`
- **Русский язык** - поля `_ru`

### Пример Модели:
\`\`\`python
class Ad(models.Model):
    name_uz = models.CharField(max_length=255)  # Узбекское название
    name_ru = models.CharField(max_length=255)  # Русское название
    description_uz = models.TextField()         # Узбекское описание
    description_ru = models.TextField()         # Русское описание
\`\`\`

## 🚀 Развертывание в Production

1. Настройте переменные окружения:
\`\`\`bash
export DJANGO_SETTINGS_MODULE=config.settings.production
\`\`\`

2. Соберите статические файлы:
\`\`\`bash
python manage.py collectstatic
\`\`\`

3. Разверните с помощью Gunicorn или uWSGI:
\`\`\`bash
gunicorn config.wsgi:application
\`\`\`

## 📊 База Данных

### SQLite для разработки
\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
\`\`\`

### PostgreSQL для продакшена
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

## 🔧 Полезные Скрипты

- `scripts/setup_database.py` - Настройка базы данных
- `scripts/load_initial_data.py` - Загрузка начальных данных
- `scripts/create_superuser.py` - Создание супер админа
- `scripts/check_categories.py` - Проверка категорий
- `scripts/test_role_permissions.py` - Тестирование разрешений

## 🤝 Внесение Вклада

1. Сделайте fork репозитория
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Поддержка

- **Email**: info@uic.group
- **Телефон**: +998 71 234 56 78
- **Telegram**: @support_77uz

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).

---

**© 2025 KirishUshbu Platform. Все права защищены.**
