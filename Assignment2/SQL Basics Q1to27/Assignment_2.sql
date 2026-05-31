CREATE DATABASE celebal_week2;

USE celebal_week2;
CREATE TABLE customers ( 
    customer_id   INT           PRIMARY KEY, 
    first_name    VARCHAR(50)   NOT NULL, 
    last_name     VARCHAR(50)   NOT NULL, 
    email         VARCHAR(100)  UNIQUE NOT NULL, 
    city          VARCHAR(50)   NOT NULL, 
    state         VARCHAR(50)   NOT NULL, 
    join_date     DATE          NOT NULL, 
    is_premium    BOOLEAN       DEFAULT FALSE 
); 
-- Index for filtering by city/state 
CREATE INDEX idx_customers_city ON customers(city); 
CREATE INDEX idx_customers_state ON customers(state); 
CREATE TABLE products ( 
    product_id    INT           PRIMARY KEY, 
    product_name  VARCHAR(100)  NOT NULL, 
    category      VARCHAR(50)   NOT NULL, 
    brand         VARCHAR(50)   NOT NULL, 
    unit_price    DECIMAL(10,2) NOT NULL  CHECK (unit_price > 0), 
    stock_qty     INT           NOT NULL  DEFAULT 0  CHECK (stock_qty >= 0) 
); 
-- Index for filtering by category 
CREATE INDEX idx_products_category ON products(category); 
CREATE TABLE orders ( 
    order_id      INT           PRIMARY KEY, 
    customer_id   INT           NOT NULL, 
    order_date    DATE          NOT NULL, 
    status        VARCHAR(20)   NOT NULL  DEFAULT 'Pending' 
                  CHECK (status IN ('Pending','Shipped','Delivered','Cancelled')), 
    total_amount  DECIMAL(12,2) NOT NULL  CHECK (total_amount >= 0), 
     
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
); 
-- Index for date-based filtering and sorting 
CREATE INDEX idx_orders_date ON orders(order_date); 
CREATE INDEX idx_orders_status ON orders(status);
CREATE TABLE order_items ( 
    item_id       INT           PRIMARY KEY, 
    order_id      INT           NOT NULL, 
    product_id    INT           NOT NULL, 
    quantity      INT           NOT NULL  CHECK (quantity > 0), 
    unit_price    DECIMAL(10,2) NOT NULL  CHECK (unit_price > 0), 
    discount_pct  DECIMAL(5,2)  DEFAULT 0 CHECK (discount_pct BETWEEN 0 AND 100), 
     
    FOREIGN KEY (order_id)   REFERENCES orders(order_id), 
    FOREIGN KEY (product_id) REFERENCES products(product_id) 
); 
SHOW TABLES;
-- ========== INSERT: customers ========== 

INSERT INTO customers VALUES 
(101, 'Aarav',  'Sharma', 'aarav.s@email.com',  'Mumbai',    'Maharashtra', '2024-01-15', TRUE), 
(102, 'Priya',  'Patel',  'priya.p@email.com',  'Ahmedabad', 'Gujarat',     '2024-02-20', FALSE), 
(103, 'Rohan',  'Gupta',  'rohan.g@email.com',  'Delhi',     'Delhi',       '2024-03-10', TRUE), 
(104, 'Sneha',  'Reddy',  'sneha.r@email.com',  'Hyderabad', 'Telangana',   '2024-04-05', FALSE), 
(105, 'Vikram', 'Singh',  'vikram.s@email.com', 'Jaipur',    'Rajasthan',   '2024-05-12', TRUE), 
(106, 'Ananya', 'Iyer',   'ananya.i@email.com', 'Chennai',   'Tamil Nadu',  '2024-06-18', FALSE), 
(107, 'Karan',  'Mehta',  'karan.m@email.com',  'Pune',      'Maharashtra', '2024-07-22', TRUE), 
(108, 'Divya',  'Nair',   'divya.n@email.com',  'Kochi',     'Kerala',      '2024-08-30', FALSE); 
-- Display all customer records

SELECT * FROM customers;
-- ========== INSERT: products ========== 
INSERT INTO products VALUES 
(201, 'Wireless Earbuds',     'Electronics', 'BoAt',          1499.00, 250), 
(202, 'Cotton T-Shirt',       'Clothing',    'Levis',         799.00,  500), 
(203, 'Smart Watch',          'Electronics', 'Noise',         2999.00, 150), 
(204, 'Running Shoes',        'Clothing',    'Nike',          4599.00, 120), 
(205, 'Bluetooth Speaker',    'Electronics', 'JBL',           3499.00, 200), 
(206, 'Bedsheet Set',         'Home',        'Spaces',        1299.00, 300), 
(207, 'Laptop Stand',         'Electronics', 'AmazonBasics',  899.00,  180), 
(208, 'Cushion Covers (Set)', 'Home',        'HomeCenter',    599.00,  400); 
SELECT * FROM products;
-- ========== INSERT: orders ========== 
INSERT INTO orders VALUES 
(1001, 101, '2024-08-01', 'Delivered',  4498.00), 
(1002, 102, '2024-08-03', 'Delivered',  799.00), 
(1003, 103, '2024-08-05', 'Shipped',    7498.00), 
(1004, 101, '2024-08-10', 'Delivered',  3499.00), 
(1005, 104, '2024-08-12', 'Cancelled',  2999.00), 
(1006, 105, '2024-08-15', 'Delivered',  5898.00), 
(1007, 106, '2024-08-18', 'Pending',    1299.00), 
(1008, 103, '2024-08-20', 'Delivered',  899.00), 
(1009, 107, '2024-08-25', 'Shipped',    6098.00), 
(1010, 108, '2024-08-28', 'Delivered',  1598.00); 
SELECT * FROM orders;
-- ========== INSERT: order_items ========== 
INSERT INTO order_items VALUES 
(5001, 1001, 201, 2, 1499.00, 0), 
(5002, 1001, 207, 1, 899.00,  10), 
(5003, 1002, 202, 1, 799.00,  0), 
(5004, 1003, 203, 1, 2999.00, 0), 
(5005, 1003, 204, 1, 4599.00, 5), 
(5006, 1004, 205, 1, 3499.00, 0), 
(5007, 1005, 203, 1, 2999.00, 0), 
(5008, 1006, 201, 1, 1499.00, 10), 
(5009, 1006, 204, 1, 4599.00, 5), 
(5010, 1007, 206, 1, 1299.00, 0), 
(5011, 1008, 207, 1, 899.00,  0), 
(5012, 1009, 205, 1, 3499.00, 0), 
(5013, 1009, 208, 2, 599.00,  15), 
(5014, 1010, 206, 1, 1299.00, 0), 
(5015, 1010, 208, 1, 599.00,  0); 

SELECT * FROM order_items;
SELECT COUNT(*) FROM customers;

SELECT COUNT(*) FROM products;

SELECT COUNT(*) FROM orders;

SELECT COUNT(*) FROM order_items;

-- SECTION A — SQL Basics (SELECT, Constraints, Primary Keys)

-- Q1. Write a query to display all columns and rows from the customers table.

SELECT * FROM customers;
-- Q2. Retrieve only the first_name, last_name, and city of all customers.

SELECT first_name, last_name, city FROM customers;
-- Q3. List all unique categories available in the products table.
SELECT DISTINCT category FROM products;
/*
Q4. Identify the Primary Key of each table in the schema.
Explain why a Primary Key must be unique and NOT NULL.

Answer:

customers   -> customer_id
products    -> product_id
orders      -> order_id
order_items -> item_id

Why UNIQUE?
1. Prevents duplicate records.
2. Uniquely identifies each row.
3. Maintains data integrity.

Why NOT NULL?
1. Every record must have an identifier.
2. NULL cannot uniquely identify a row.
3. Required for establishing relationships.
*/

/*
Q5. What constraints are applied to the email column in
the customers table? What would happen if you tried to
insert a duplicate email?

Answer:

Constraints:
1. UNIQUE
2. NOT NULL

If a duplicate email is inserted,
the database throws a duplicate entry error
and rejects the record.
*/
-- Attempt Duplicate Email

INSERT INTO customers VALUES
(
109,
'Test',
'User',
'aarav.s@email.com',
'Delhi',
'Delhi',
'2024-09-01',
TRUE
);
/*Q6. Try inserting a product with unit_price = -50.
What happens and which constraint prevents it?
*/

-- INSERT INTO products VALUES ( 209, 'Test Product', 'Electronics', 'TestBrand', -50, 100 );

/*
Expected Result:
The insertion fails.

Reason:

CHECK (unit_price > 0)

The CHECK constraint prevents negative values
from being inserted into unit_price.
*/
-- =========================================
-- Q6. Test CHECK Constraint
-- =========================================

INSERT INTO products VALUES
(
209,
'Invalid Product',
'Electronics',
'TestBrand',
-50,
100
);

-- SECTION B — Filtering & Optimization (WHERE, Indexes) 

-- Q7. Retrieve all orders with status = 'Delivered'. 
SELECT *
FROM orders
WHERE status = 'Delivered';

-- Q8. Find all products in the 'Electronics' category with a unit_price greater than ₹2000. 
SELECT *
FROM products
WHERE category = 'Electronics'
AND unit_price > 2000;

-- Q9. List all customers who joined in the year 2024 and belong to the state 'Maharashtra'.
SELECT *
FROM customers
WHERE state = 'Maharashtra'
AND YEAR(join_date) = 2024;

-- Q10. Find all orders placed between '2024-08-10' and '2024-08-25' (inclusive) that are NOT cancelled.
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
AND status <> 'Cancelled';

-- Q11. Explain what the index idx_orders_date does. How would it improve the performance of a query that filters orders by order_date? Write a sample query that would benefit from this index. 
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-01'
AND '2024-08-31';
/* idx_orders_date index helps MySQL quickly locate rows
without scanning the entire orders table.

Benefits:
1. Faster filtering
2. Faster sorting
3. Improved query performance */

-- Q12. If you run: SELECT * FROM customers WHERE YEAR(join_date) = 2024; — would the index on join_date be used? Explain why or why not, and rewrite the query to be index-friendly (SARGable).
-- Non-SARGable
SELECT *
FROM customers
WHERE YEAR(join_date) = 2024;
-- SARGable Version
SELECT *
FROM customers
WHERE join_date >= '2024-01-01'
AND join_date < '2025-01-01';

-- Section C — Aggregation (GROUP BY, SUM, COUNT, AVG, MIN, MAX) 
-- Q13. Count the total number of orders in the orders table.
SELECT COUNT(*) AS total_orders
FROM orders;

-- Q14. Find the total revenue (SUM of total_amount) from all 'Delivered' orders. 
SELECT SUM(total_amount) AS delivered_revenue
FROM orders
WHERE status = 'Delivered'; 
-- Q15. Calculate the average unit_price of products in each category.
SELECT
    category,
    AVG(unit_price) AS average_price
FROM products
GROUP BY category; 
-- Q16. For each order status, find the count of orders and the total revenue. Sort the result by total revenue in descending order.
SELECT
    status,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC; 

-- Q17. Find the most expensive (MAX) and cheapest (MIN) product in each category. 
SELECT
    category,
    MAX(unit_price) AS highest_price,
    MIN(unit_price) AS lowest_price
FROM products
GROUP BY category;

-- Q18. List all product categories where the average unit_price is greater than ₹2000. (Hint: Use HAVING clause) 
SELECT
    category,
    AVG(unit_price) AS average_price
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;

-- Section D — Joins & Relationships
-- Q19. Write an INNER JOIN query to display each order along with the customer's first_name and last_name. Show: order_id, order_date, first_name, last_name, total_amount. 
SELECT
    o.order_id,
    o.order_date,
    c.first_name,
    c.last_name,
    o.total_amount
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id;

-- Q20. Using a LEFT JOIN, list ALL customers and their orders (if any). Customers with no orders should still appear with NULL values for order columns.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    o.order_id,
    o.order_date,
    o.status
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

-- Q21. Write a query using JOINs across three tables (orders → order_items → products) to show: order_id, product_name, quantity, unit_price, and discount_pct for each order item. 
SELECT
    o.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id;

-- Q22. Explain the difference between LEFT JOIN and RIGHT JOIN with an example from this schema. When would you use a FULL OUTER JOIN?
/* LEFT JOIN:
Returns all records from the left table and matching records from the right table.

Example:
customers LEFT JOIN orders

All customers will appear even if they have no orders.

RIGHT JOIN:
Returns all records from the right table and matching records from the left table.

Example:
customers RIGHT JOIN orders

All orders will appear even if customer information is missing.

FULL OUTER JOIN:
Returns all matching and non-matching rows from both tables.

Used when we need complete data from both tables. */

-- Q23. Identify all Foreign Key relationships in the schema. Explain what would happen if you tried to insert an order with customer_id = 999 (which doesn't exist in customers).
 /* Foreign Key Relationships:

1. orders.customer_id
   references customers.customer_id

2. order_items.order_id
   references orders.order_id

3. order_items.product_id
   references products.product_id

If customer_id = 999 does not exist in customers table,
MySQL will throw a Foreign Key Constraint Error
and the record will not be inserted. */

/* The orders table contains a foreign key customer_id
which references customers.customer_id.

If we try to insert an order with customer_id = 999,
and no such customer exists in the customers table,
MySQL rejects the insertion and raises a Foreign Key
Constraint Error.

This ensures referential integrity and prevents
orphan records in the database. */

-- Section E — Advanced Concepts (CASE, ACID, Transactions)
 -- =========================================
-- Q24. Classify Products into Price Tiers
-- =========================================

SELECT
    product_name,
    unit_price,
    CASE
        WHEN unit_price < 1000 THEN 'Budget'
        WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
        ELSE 'Premium'
    END AS price_tier
FROM products;
-- =========================================
-- Q25. Delivered vs Not Delivered Orders
-- =========================================

SELECT
    SUM(CASE
            WHEN status = 'Delivered'
            THEN 1
            ELSE 0
        END) AS delivered_orders,

    SUM(CASE
            WHEN status <> 'Delivered'
            THEN 1
            ELSE 0
        END) AS not_delivered_orders
FROM orders;

-- Q26. Explain each letter of ACID: 

/* A – Atomicity
A transaction is completed entirely or not at all.

Example:
If money is deducted from Account A but not credited
to Account B due to failure, the entire transaction
is rolled back.
C – Consistency
A transaction must keep the database in a valid state.

Example:
After a bank transfer, total money in the system
remains unchanged.
I – Isolation
Multiple transactions should not interfere with each other.

Example:
Two users withdrawing money simultaneously should not
see inconsistent balances.
D – Durability
Once a transaction is committed, it remains saved
even after system crashes.

Example:
Completed bank transfer remains recorded after power failure.  */

-- =========================================
-- Q27. Transaction Example
-- =========================================

START TRANSACTION;

-- Step 1: Create New Order

INSERT INTO orders
(order_id, customer_id, order_date, status, total_amount)
VALUES
(1011, 102, CURDATE(), 'Pending', 1598.00);

-- Step 2: Insert Order Items

INSERT INTO order_items
(item_id, order_id, product_id, quantity, unit_price, discount_pct)
VALUES
(5016, 1011, 206, 1, 1299.00, 0);

INSERT INTO order_items
(item_id, order_id, product_id, quantity, unit_price, discount_pct)
VALUES
(5017, 1011, 208, 1, 299.00, 0);

-- Step 3: Update Stock

UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 206;

UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 208;

COMMIT; 

-- rollback
START TRANSACTION;

INSERT INTO orders
(order_id, customer_id, order_date, status, total_amount)
VALUES
(1012, 102, CURDATE(), 'Pending', 1000);

ROLLBACK;

SELECT *
FROM orders
WHERE order_id = 1012;