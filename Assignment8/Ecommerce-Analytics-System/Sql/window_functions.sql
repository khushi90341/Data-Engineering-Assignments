-- ==========================================================
-- E-Commerce Analytics System
-- File: window_functions.sql
-- Purpose: Advanced SQL Queries (Window Functions & CTEs)
-- ==========================================================

-- ==========================================================
-- Q7. Running Total of Revenue Per Region
-- ==========================================================

WITH daily_revenue AS (

    SELECT

        o.region_code,

        DATE(o.order_date) AS order_date,

        ROUND(

            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            ),

            2

        ) AS daily_revenue

    FROM orders o

    JOIN order_items oi
    ON o.order_id = oi.order_id

    GROUP BY
        o.region_code,
        DATE(o.order_date)

)

SELECT
    region_code,
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        PARTITION BY region_code
        ORDER BY order_date
    ) AS running_total
FROM daily_revenue
ORDER BY region_code, order_date;
-- ==========================================================
-- Q8. Rank Products By Revenue (DENSE_RANK)
-- ==========================================================

SELECT

    p.category,

    p.product_name,

    ROUND(

        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent/100.0)
        ),

        2

    ) AS total_revenue,

    DENSE_RANK() OVER(

        PARTITION BY p.category

        ORDER BY

        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent/100.0)
        ) DESC

    ) AS rank_in_category

FROM products p

JOIN order_items oi

ON p.product_id = oi.product_id

GROUP BY

    p.category,

    p.product_name;

-- ==========================================================
-- Q9. Days Between Consecutive Orders (LAG)
-- ==========================================================

WITH customer_orders AS (

SELECT

    customer_id,

    DATE(order_date) AS order_date,

    LAG(DATE(order_date))

    OVER(

        PARTITION BY customer_id

        ORDER BY DATE(order_date)

    )

    AS previous_order_date

FROM orders

WHERE customer_id != -1

)

SELECT

    customer_id,

    order_date,

    previous_order_date,

    JULIANDAY(order_date) -

    JULIANDAY(previous_order_date)

    AS days_gap

FROM customer_orders;

-- ==========================================================
-- Q10. Multi-Level CTE: Monthly Revenue & Customer Category
-- ==========================================================

WITH monthly_revenue AS (

    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month,

        ROUND(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS monthly_revenue

    FROM orders o

    JOIN order_items oi
    ON o.order_id = oi.order_id

    WHERE o.customer_id != -1

    GROUP BY
        o.customer_id,
        order_month
),

customer_category AS (

    SELECT

        customer_id,

        order_month,

        monthly_revenue,

        CASE

            WHEN monthly_revenue > 10000 THEN 'High'

            WHEN monthly_revenue BETWEEN 5000 AND 10000 THEN 'Medium'

            ELSE 'Low'

        END AS customer_segment

    FROM monthly_revenue

)

SELECT

    order_month,

    customer_segment,

    COUNT(*) AS total_customers

FROM customer_category

GROUP BY

    order_month,

    customer_segment

ORDER BY

    order_month,

    customer_segment;

    
    -- ==========================================================
-- Q12. Year-over-Year Revenue Comparison
-- ==========================================================

WITH yearly_revenue AS (

SELECT

    strftime('%Y', order_date) AS year,

    strftime('%m', order_date) AS month,

    ROUND(

        SUM(

            oi.quantity *

            oi.unit_price *

            (1 - oi.discount_percent /100.0)

        ),

        2

    ) AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY

    year,

    month

)

SELECT

    current.year,

    current.month,

    current.revenue,

    previous.revenue AS prev_year_revenue,

    ROUND(

        (

            (current.revenue-previous.revenue)

            *100.0

            /

            previous.revenue

        ),

        2

    ) AS yoy_growth_percent

FROM yearly_revenue current

LEFT JOIN yearly_revenue previous

ON current.month=previous.month

AND current.year=CAST(previous.year AS INTEGER)+1;

-- ==========================================================
-- Q13. First Purchased Category vs Latest Purchased Category
-- ==========================================================

WITH customer_category AS (

    SELECT
        o.customer_id,
        DATE(o.order_date) AS order_date,
        p.category,

        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY DATE(o.order_date)
        ) AS first_category,

        LAST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY DATE(o.order_date)
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND UNBOUNDED FOLLOWING
        ) AS last_category

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    WHERE o.customer_id != -1
)

SELECT DISTINCT

    customer_id,

    first_category,

    last_category,

    CASE

        WHEN first_category = last_category

        THEN 'No'

        ELSE 'Yes'

    END AS category_shift

FROM customer_category;

-- ==========================================================
-- Q14. Cumulative Revenue Distribution
-- ==========================================================

WITH customer_revenue AS (

    SELECT

        o.customer_id,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent/100.0)

            ),

            2

        ) AS revenue

    FROM orders o

    JOIN order_items oi

        ON o.order_id = oi.order_id

    WHERE o.customer_id != -1

    GROUP BY o.customer_id

)

SELECT

    customer_id,

    revenue,

    SUM(revenue)

        OVER(

            ORDER BY revenue DESC

        ) AS cumulative_revenue,

    ROUND(

        100.0 *

        SUM(revenue)

            OVER(

                ORDER BY revenue DESC

            )

        /

        SUM(revenue)

            OVER(),

        2

    ) AS cumulative_percent

FROM customer_revenue

ORDER BY revenue DESC;

-- ==========================================================
-- Q15. Days Between Consecutive Orders (At Risk Customers)
-- ==========================================================

WITH order_gap AS (

    SELECT

        customer_id,

        DATE(order_date) AS order_date,

        JULIANDAY(DATE(order_date))

        -

        JULIANDAY(

            LAG(DATE(order_date))

            OVER(

                PARTITION BY customer_id

                ORDER BY DATE(order_date)

            )

        ) AS days_gap

    FROM orders

    WHERE customer_id != -1

)

SELECT

    customer_id,

    ROUND(AVG(days_gap),2) AS average_gap,

    CASE

        WHEN AVG(days_gap) > 30

        THEN 'At Risk'

        ELSE 'Active'

    END AS customer_status

FROM order_gap

GROUP BY customer_id;