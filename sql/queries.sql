-- 1. ВЫБОРКА СПИСКА (SELECT): Все поставщики
SELECT id, name, inn FROM suppliers ORDER BY name;

-- 2. ВЫБОРКА СПИСКА (SELECT): Все товары с ценами
SELECT id, name, price, stock FROM products ORDER BY price DESC;

-- 3. ФИЛЬТРАЦИЯ (WHERE): Поставщики с заданным ИНН
SELECT id, name FROM suppliers WHERE inn = ?;

-- 4. ФИЛЬТРАЦИЯ (WHERE): Товары с остатком меньше 10
SELECT name, stock FROM products WHERE stock < 10;

-- 5. СОЕДИНЕНИЕ (JOIN): Вывод товаров с названиями поставщиков
SELECT p.name AS product_name, p.price, s.name AS supplier_name
FROM products p
JOIN suppliers s ON p.supplier_id = s.id
ORDER BY s.name;

-- 6. СОЕДИНЕНИЕ (JOIN): Договоры с именами поставщиков
SELECT c.number, c.start_date, c.status, s.name AS supplier_name
FROM contracts c
JOIN suppliers s ON c.supplier_id = s.id
WHERE c.status = 'active'; -- Предполагается, что статус хранится текстом

-- 7. АГРЕГАЦИЯ (COUNT): Общее количество товаров
SELECT COUNT(*) AS total_products FROM products;

-- 8. АГРЕГАЦИЯ (SUM/AVG): Общая стоимость всех товаров на складе
SELECT SUM(price * stock) AS total_inventory_value FROM products;

-- 9. ГРУППИРОВКА (GROUP BY): Количество товаров у каждого поставщика
SELECT s.name AS supplier_name, COUNT(p.id) AS product_count
FROM suppliers s
LEFT JOIN products p ON s.id = p.supplier_id
GROUP BY s.id, s.name
ORDER BY product_count DESC;

-- 10. ГРУППИРОВКА (GROUP BY + HAVING): Поставщики, у которых больше 2 товаров
SELECT s.name AS supplier_name, COUNT(p.id) AS product_count
FROM suppliers s
JOIN products p ON s.id = p.supplier_id
GROUP BY s.id, s.name
HAVING COUNT(p.id) > 2;