-- =========================================
-- WEEK 3 INTERNSHIP ASSIGNMENT
-- TOPIC: Superstore SQL Analysis
-- =========================================


-- Create Database

CREATE DATABASE superstore_analysis;

-- Use Database

USE superstore_analysis;
USE superstore_analysis;

SELECT *
FROM superstore_raw
LIMIT 10;


-- Step 1 : Setup Data


--  Create Customers Table

CREATE TABLE customers (
    customer_id VARCHAR(30),
    customer_name VARCHAR(100),
    segment VARCHAR(50)
);
--  Insert Unique Customers
-- Using SELECT DISTINCT

INSERT INTO customers

SELECT DISTINCT
    `Customer ID`,
    `Customer Name`,
    Segment

FROM superstore_raw;

-- Verify Customers Data
SELECT *
FROM customers
LIMIT 10;

--  Create Orders Table

CREATE TABLE orders (
    row_id INT,
    order_id VARCHAR(50),
    order_date VARCHAR(50),
    ship_date VARCHAR(50),
    ship_mode VARCHAR(50),
    customer_id VARCHAR(50),
    sales DOUBLE,
    quantity INT,
    discount DOUBLE,
    profit DOUBLE
);

-- Insert Orders Data
-- Using SELECT DISTINCT

INSERT INTO orders

SELECT DISTINCT
    `Row ID`,
    `Order ID`,
    `Order Date`,
    `Ship Date`,
    `Ship Mode`,
    `Customer ID`,
    Sales,
    Quantity,
    Discount,
    Profit

FROM superstore_raw;

-- Verify Orders Data

SELECT *
FROM orders
LIMIT 10;

--  Create Products Table

CREATE TABLE products (
    product_id VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name TEXT
);

--  Insert Unique Products
-- Using SELECT DISTINCT

INSERT INTO products

SELECT DISTINCT
    `Product ID`,
    Category,
    `Sub-Category`,
    `Product Name`

FROM superstore_raw;

-- Verify Products Table
SELECT *
FROM products
LIMIT 10;

SHOW TABLES;

-- Step 2: Perform Required Queries 
-- Query 1 : Find orders greater than average sales.
-- Orders Above Average Sales

SELECT *
FROM orders
WHERE sales >
(
    SELECT AVG(sales)
    FROM orders
);
-- verify
SELECT COUNT(*)
FROM orders
WHERE sales >
(
    SELECT AVG(sales)
    FROM orders
);

-- Query 2: Highest Sales Order Per Customer
-- Using Correlated Subquery

SELECT *
FROM orders o

WHERE sales =
(
    SELECT MAX(sales)
    FROM orders
    WHERE customer_id = o.customer_id
);
-- Query 3: Total Sales Per Customer
-- Using CTE

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM customer_sales;

-- Query 4: Customers Above Average Sales
-- Using CTE + Subquery

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM customer_sales

WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);

-- Query 5: Customer Ranking
-- Using RANK()

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    total_sales,

    RANK() OVER
    (
        ORDER BY total_sales DESC
    ) AS sales_rank

FROM customer_sales;
-- Query 6: Row Number Per Customer
-- Using ROW_NUMBER()

SELECT
    customer_id,
    order_id,
    sales,

    ROW_NUMBER() OVER
    (
        PARTITION BY customer_id
        ORDER BY sales DESC
    ) AS row_num

FROM orders;
-- Query 7: Top 3 Customers
-- Using Window Function

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM
(
    SELECT
        customer_id,
        total_sales,

        RANK() OVER
        (
            ORDER BY total_sales DESC
        ) AS ranking

    FROM customer_sales
) ranked_customers

WHERE ranking <= 3;

-- Step 3: Final Combined Query
 
-- Final Combined Query
-- JOIN + CTE + Window Function

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT

    c.customer_name,

    cs.total_sales,

    RANK() OVER
    (
        ORDER BY cs.total_sales DESC
    ) AS customer_rank

FROM customer_sales cs

JOIN customers c
ON cs.customer_id = c.customer_id

ORDER BY customer_rank;

-- Mini Project: Customer Sales Insights 
-- Top 5 Customers

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM customer_sales

ORDER BY total_sales DESC

LIMIT 5;
-- Bottom 5 Customers

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM customer_sales

ORDER BY total_sales ASC

LIMIT 5;
-- Customers Who Made Only One Order

SELECT
    customer_id,
    COUNT(order_id) AS total_orders

FROM orders

GROUP BY customer_id

HAVING COUNT(order_id) = 1;

-- Above Average Customers

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM customer_sales

WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);
-- Highest Order Value Per Customer

SELECT
    customer_id,
    MAX(sales) AS highest_order_value

FROM orders

GROUP BY customer_id;

--  Brief Insights
-- 1. Some customers contribute significantly higher sales than the average customer.

-- 2. Customer sales distribution is uneven, with a few customers generating a large share of total revenue.

-- 3. Several customers have only one order, indicating opportunities for customer retention strategies.

-- 4. Top-ranked customers can be targeted for loyalty programs and premium offers.

-- 5. Customers with above-average sales contribute strongly to overall business performance.

-- 6. Product and customer data were normalized into separate tables (customers, orders, products) for efficient analysis.