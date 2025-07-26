-- Regions va districts uchun to'g'ri data
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
('Toshkent viloyati / Ташкентская область', NOW())
ON CONFLICT DO NOTHING;

-- Districts for Tashkent city
INSERT INTO districts (region_id, name, created_at) VALUES
(1, 'Chilonzor tumani / Чиланзарский район', NOW()),
(1, 'Mirobod tumani / Мирабадский район', NOW()),
(1, 'Yunusobod tumani / Юнусабадский район', NOW()),
(1, 'Shayxontohur tumani / Шайхантахурский район', NOW()),
(1, 'Olmazor tumani / Алмазарский район', NOW()),
(1, 'Bektemir tumani / Бектемирский район', NOW()),
(1, 'Uchtepa tumani / Учтепинский район', NOW()),
(1, 'Yakkasaray tumani / Яккасарайский район', NOW()),
(1, 'Yashnobod tumani / Яшнабадский район', NOW()),
(1, 'Sergeli tumani / Сергелийский район', NOW())
ON CONFLICT DO NOTHING;

-- Categories
INSERT INTO categories (name, is_active, created_at) VALUES
('Elektronika / Электроника', true, NOW()),
('Kiyim-kechak / Одежда', true, NOW()),
('Uy-ro''zg''or buyumlari / Товары для дома', true, NOW()),
('Sport va dam olish / Спорт и отдых', true, NOW()),
('Avtomobillar / Автомобили', true, NOW()),
('Ko''chmas mulk / Недвижимость', true, NOW()),
('Xizmatlar / Услуги', true, NOW())
ON CONFLICT DO NOTHING;

-- Static pages
INSERT INTO static_pages (slug, title, content, created_at, updated_at) VALUES
('about-us', 'Biz haqimizda / О нас', '77.uz - O''zbekistondagi eng yirik onlayn bozor. Мы крупнейший онлайн-рынок в Узбекистане.', NOW(), NOW()),
('privacy-policy', 'Maxfiylik siyosati / Политика конфиденциальности', 'Maxfiylik siyosati matni...', NOW(), NOW()),
('terms-of-service', 'Foydalanish shartlari / Условия использования', 'Foydalanish shartlari matni...', NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- Settings
INSERT INTO settings (phone, support_email, working_hours, app_version, maintenance_mode) VALUES
('+998712345678', 'support@77.uz', 'Dushanba-Yakshanba 9:00-21:00 / Пн-Вс 9:00-21:00', '1.0.0', false)
ON CONFLICT DO NOTHING;
