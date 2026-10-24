-- 0. Удаление старых версий таблиц для предотвращения конфликтов имен при перезапуске
DROP TABLE IF EXISTS products, categories CASCADE;

-- 1. Создание родительской таблицы (Категории)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Создание дочерней таблицы (Товары) со связью FOREIGN KEY
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(category_id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0)
);
