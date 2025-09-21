-- 1
SELECT c.name AS client_name, SUM(oi.quantity * oi.price_at_order) AS total_amount
FROM clients c
JOIN orders o ON o.client_id = c.id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY c.id
ORDER BY total_amount DESC;

-- 2
SELECT parent.id AS category_id, parent.name AS category_name, COUNT(child.id) AS children_count
FROM categories parent
JOIN category_closure cc ON cc.ancestor_id = parent.id AND cc.depth = 1
JOIN categories child ON child.id = cc.descendant_id
GROUP BY parent.id
ORDER BY parent.id;

-- 3.1
CREATE OR REPLACE VIEW top5_products_last_month AS
SELECT p.name AS product_name, root_cat.name AS root_category_name, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN products p ON p.id = oi.product_id
JOIN product_categories pc ON pc.product_id = p.id
JOIN category_closure cc ON cc.descendant_id = pc.category_id
JOIN categories root_cat ON root_cat.id = cc.ancestor_id
WHERE cc.depth = (
        SELECT MIN(cc2.depth)
        FROM category_closure cc2
        WHERE cc2.descendant_id = pc.category_id
    )
    AND o.order_date >= (CURRENT_DATE - INTERVAL '1 month')
GROUP BY p.id
ORDER BY total_sold DESC
LIMIT 5;

-- 3.2
-- Оптимизация:
-- 1. Добавить в products колонку root_category_id, это позволит убрать вычисление корневой категории для отчета
-- 2. Добавить индекс на (order_date) в таблицу orders для ускорения фильтрации по дате
-- 3. Создать materialized view для top5_products_last_month и обновлять по расписанию.
-- Это позволит формировать отчет быстрее по запросу.
