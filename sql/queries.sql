SELECT id, name, inn FROM suppliers ORDER BY name;

SELECT id, name, price, stock FROM products ORDER BY price DESC;

SELECT id, name FROM suppliers WHERE inn = ?;

SELECT name, stock FROM products WHERE stock < 10;

SELECT p.name AS product_name, p.price, s.name AS supplier_name
FROM products p
JOIN suppliers s ON p.supplier_id = s.id
ORDER BY s.name;

SELECT c.number, c.start_date, c.status, s.name AS supplier_name
FROM contracts c
JOIN suppliers s ON c.supplier_id = s.id
WHERE c.status = 'active';

SELECT COUNT(*) AS total_products FROM products;

SELECT SUM(price * stock) AS total_inventory_value FROM products;

SELECT s.name AS supplier_name, COUNT(p.id) AS product_count
FROM suppliers s
LEFT JOIN products p ON s.id = p.supplier_id
GROUP BY s.id, s.name
ORDER BY product_count DESC;

SELECT s.name AS supplier_name, COUNT(p.id) AS product_count
FROM suppliers s
JOIN products p ON s.id = p.supplier_id
GROUP BY s.id, s.name
HAVING COUNT(p.id) > 2;