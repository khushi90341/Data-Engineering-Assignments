-- ==========================================================
-- E-Commerce Analytics System
-- File: aggregations.sql
-- Purpose: Basic and Intermediate SQL Queries
-- ==========================================================

-- ==========================================================
-- Q1. Total Revenue Per Category
-- Revenue = Quantity × Unit Price × (1 - Discount/100)
-- ==========================================================

SELECT
    p.category,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- ==========================================================
-- Q2. Top 10 Customers By Total Order Value
-- ==========================================================

SELECT
    c.customer_id,
    c.customer_name,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_order_value
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_order_value DESC
LIMIT 10;

-- ==========================================================
-- Q3. Month-wise Order Count (Last 12 Months)
-- ==========================================================

SELECT
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(*) AS total_orders
FROM orders
WHERE date(order_date) >= date('now','-12 months')
GROUP BY order_month
ORDER BY order_month;

-- ==========================================================
-- Q4. Customers Who Placed Orders
-- But Never Had Any Item Delivered
-- ==========================================================

SELECT DISTINCT
    c.customer_id,
    c.customer_name
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
WHERE c.customer_id NOT IN (

    SELECT DISTINCT customer_id

    FROM orders

    WHERE status='DELIVERED'
);

-- ==========================================================
-- Q5. Products Having More Returns Than Purchases
-- ==========================================================

SELECT

    p.product_id,

    p.product_name,

    SUM(
        CASE
            WHEN oi.quantity < 0
            THEN ABS(oi.quantity)
            ELSE 0
        END
    ) AS returned_items,

    SUM(
        CASE
            WHEN oi.quantity > 0
            THEN oi.quantity
            ELSE 0
        END
    ) AS purchased_items

FROM products p

JOIN order_items oi

ON p.product_id = oi.product_id

GROUP BY

    p.product_id,

    p.product_name

HAVING

    returned_items > purchased_items;

-- ==========================================================
-- Q6. Return Rate Per Category
-- ==========================================================

SELECT

    p.category,

    ROUND(

        (
            SUM(
                CASE
                    WHEN oi.quantity < 0
                    THEN ABS(oi.quantity)
                    ELSE 0
                END
            )

            *100.0

            /

            SUM(ABS(oi.quantity))

        ),

        2

    ) AS return_rate

FROM products p

JOIN order_items oi

ON p.product_id = oi.product_id

GROUP BY

    p.category

ORDER BY

    return_rate DESC;