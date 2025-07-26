-- Insert initial regions and districts
INSERT INTO regions (name, created_at) VALUES
('Toshkent shahar / г. Ташкент', NOW()),
('Andijon viloyati / Андижанская область', NOW()),
('Buxoro viloyati / Бухарская область', NOW()),
('Farg''ona viloyati / Ферганская область', NOW()),
('Jizzax viloyati / Джизакская область', NOW()),
('Xorazm viloyati / Хорезмская область', NOW()),
('Namangan viloyati / Наманганская область', NOW()),
('Navoiy viloyati / Навоийская область', NOW()),
('Qashqadaryo viloyati / Кашкадарьинская область', NOW()),
('Qoraqalpog''iston Respublikasi / Республика Каракалпакстан', NOW()),
('Samarqand viloyati / Самаркандская область', NOW()),
('Sirdaryo viloyati / Сырдарьинская область', NOW()),
('Surxondaryo viloyati / Сурхандарьинская область', NOW()),
('Toshkent viloyati / Ташкентская область', NOW());

-- Insert districts for Tashkent city
INSERT INTO districts (region_id, name, created_at) VALUES
(1, 'Chilonzor tumani / Чиланзарский район', NOW()),
(1, 'Mirobod tumani / Мирабадский район', NOW()),
(1, 'Yunusobod tumani / Юнусабадский район', NOW()),
(1, 'Shayxontohur tumani / Шайхантахурский район', NOW()),
(1, 'Olmazor tumani / Алмазарский район', NOW()),
(1, 'Bektemir tumani / Бектемирский район', NOW()),
(1, 'Uchtepa tumani / Учтепинский район', NOW()),
(1, 'Yakkasaroy tumani / Яккасарайский район', NOW()),
(1, 'Yashnobod tumani / Яшнабадский район', NOW()),
(1, 'Sergeli tumani / Сергелийский район', NOW()),
(1, 'Yashnaobod tumani / Яшнаабадский район', NOW());

-- Insert main categories
INSERT INTO categories (name, is_active, created_at) VALUES
('Elektronika / Электроника', true, NOW()),
('Kiyim-kechak / Одежда', true, NOW()),
('Uy-ro''zg''or buyumlari / Товары для дома', true, NOW()),
('Sport va dam olish / Спорт и отдых', true, NOW()),
('Avtomobillar / Автомобили', true, NOW()),
('Ko''chmas mulk / Недвижимость', true, NOW()),
('Xizmatlar / Услуги', true, NOW());

-- Insert subcategories for Electronics
INSERT INTO categories (name, parent_id, is_active, created_at) VALUES
('Telefonlar / Телефоны', 1, true, NOW()),
('Noutbuklar / Ноутбуки', 1, true, NOW()),
('Televizorlar / Телевизоры', 1, true, NOW()),
('Muzlatgichlar / Холодильники', 1, true, NOW()),
('Kir yuvish mashinalari / Стиральные машины', 1, true, NOW());

-- Insert subcategories for Clothing
INSERT INTO categories (name, parent_id, is_active, created_at) VALUES
('Erkaklar kiyimi / Мужская одежда', 2, true, NOW()),
('Ayollar kiyimi / Женская одежда', 2, true, NOW()),
('Bolalar kiyimi / Детская одежда', 2, true, NOW()),
('Poyabzallar / Обувь', 2, true, NOW());

-- Insert static pages
INSERT INTO static_pages (slug, title, content, created_at, updated_at) VALUES
('about-us', 'Biz haqimizda / О нас', '77.uz - O''zbekistondagi eng yirik onlayn bozor. Мы крупнейший онлайн-рынок в Узбекистане.', NOW(), NOW()),
('privacy-policy', 'Maxfiylik siyosati / Политика конфиденциальности', 'Maxfiylik siyosati matni...', NOW(), NOW()),
('terms-of-service', 'Foydalanish shartlari / Условия использования', 'Foydalanish shartlari matni...', NOW(), NOW());

-- Insert application settings
INSERT INTO settings (phone, support_email, working_hours, app_version, maintenance_mode) VALUES
('+998712345678', 'support@77.uz', 'Dushanba-Yakshanba 9:00-21:00 / Пн-Вс 9:00-21:00', '1.0.0', false);

-- Insert popular search terms
INSERT INTO popular_search_terms (name, search_count, updated_at) VALUES
('iPhone / Айфон', 15234, NOW()),
('Samsung Galaxy / Самсунг Галакси', 12456, NOW()),
('Noutbuk / Ноутбук', 9876, NOW()),
('Kiyim / Одежда', 8765, NOW()),
('Avtomobil / Автомобиль', 7654, NOW());
