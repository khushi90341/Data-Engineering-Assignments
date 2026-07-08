-- ==========================================================
-- E-Commerce Analytics System
-- File: cohort_analysis.sql
-- Purpose: Cohort & Retention Analysis
-- ==========================================================

-- ==========================================================
-- Q16. Cohort Analysis
-- ==========================================================

WITH first_purchase AS (

    -- Find each customer's first purchase month
    SELECT

        customer_id,

        MIN(DATE(order_date)) AS first_purchase_date,

        strftime('%Y-%m', MIN(DATE(order_date))) AS cohort_month

    FROM orders

    WHERE customer_id != -1

    GROUP BY customer_id

),

customer_orders AS (

    -- Get every customer's order month
    SELECT

        o.customer_id,

        fp.cohort_month,

        strftime('%Y-%m', DATE(o.order_date)) AS order_month,

        (
            (CAST(strftime('%Y', DATE(o.order_date)) AS INTEGER) -
             CAST(strftime('%Y', fp.first_purchase_date) AS INTEGER)) * 12

            +

            (CAST(strftime('%m', DATE(o.order_date)) AS INTEGER) -
             CAST(strftime('%m', fp.first_purchase_date) AS INTEGER))

        ) AS month_number

    FROM orders o

    JOIN first_purchase fp

        ON o.customer_id = fp.customer_id

),

cohort_retention AS (

    SELECT

        cohort_month,

        month_number,

        COUNT(DISTINCT customer_id) AS customers

    FROM customer_orders

    GROUP BY

        cohort_month,

        month_number

)

SELECT

    cohort_month,

    SUM(CASE WHEN month_number = 0 THEN customers ELSE 0 END) AS month_0,

    SUM(CASE WHEN month_number = 1 THEN customers ELSE 0 END) AS month_1,

    SUM(CASE WHEN month_number = 2 THEN customers ELSE 0 END) AS month_2,

    SUM(CASE WHEN month_number = 3 THEN customers ELSE 0 END) AS month_3,

    ROUND(

        100.0 *

        SUM(CASE WHEN month_number = 1 THEN customers ELSE 0 END)

        /

        NULLIF(

            SUM(CASE WHEN month_number = 0 THEN customers ELSE 0 END),

            0

        ),

        2

    ) AS retention_rate_month1

FROM cohort_retention

GROUP BY cohort_month

ORDER BY cohort_month;