# Databricks notebook source
# MAGIC %md
# MAGIC ### # ==========================================================
# MAGIC ### # SHADOW REVENUE DETECTION SYSTEM
# MAGIC ### # Notebook 04 : Spark SQL Analytics
# MAGIC ### #
# MAGIC ### # Objective:
# MAGIC ### # Register Gold Layer datasets as SQL views and perform
# MAGIC ### # business analytics using Spark SQL.
# MAGIC ### # ==========================================================

# COMMAND ----------

# ==========================================================
# Step 1 : Load Gold Layer Data
# ==========================================================

fact_good = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/gold/fact_revenue_good"
)

fact_bad = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/gold/fact_revenue_bad"
)

kpi_good = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/gold/kpi_revenue_good"
)

kpi_bad = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/gold/kpi_revenue_bad"
)


# COMMAND ----------

# ==========================================================
# Step 2 : Register SQL Views
# ==========================================================

fact_good.createOrReplaceTempView("fact_revenue_good")

fact_bad.createOrReplaceTempView("fact_revenue_bad")

kpi_good.createOrReplaceTempView("kpi_revenue_good")

kpi_bad.createOrReplaceTempView("kpi_revenue_bad")

print("✅ SQL Views Created")

# COMMAND ----------

# ==========================================================
# Query 1
# KPI Comparison (Bad vs Good Pipeline)
# ==========================================================

kpi_comparison = spark.sql("""

SELECT
'Bad' AS version,
total_revenue,
total_payment,
revenue_difference,
accuracy_ratio
FROM kpi_revenue_bad

UNION ALL

SELECT
'Good',
total_revenue,
total_payment,
revenue_difference,
accuracy_ratio
FROM kpi_revenue_good

""")

display(kpi_comparison)

# COMMAND ----------

# ==========================================================
# Query 2
# Missing Payments Comparison
# ==========================================================

missing_payments = spark.sql("""

SELECT
'Bad' AS pipeline,
COUNT(*) AS missing_payments
FROM fact_revenue_bad
WHERE payment_amount IS NULL

UNION ALL

SELECT
'Good',
COUNT(*)
FROM fact_revenue_good
WHERE payment_amount IS NULL

""")

display(missing_payments)

# COMMAND ----------

spark.sql("SHOW TABLES").display()

# COMMAND ----------

# ==========================================================
# Query 3
# Missing Payments Comparison
# ==========================================================

query = """
SELECT
    'Bad' AS pipeline,
    COUNT(*) AS missing_payments
FROM fact_revenue_bad
WHERE payment_amount IS NULL

UNION ALL

SELECT
    'Good' AS pipeline,
    COUNT(*) AS missing_payments
FROM fact_revenue_good
WHERE payment_amount IS NULL
"""

display(spark.sql(query))

# COMMAND ----------

# ==========================================================
# Query 4
# Price Mismatch Comparison
# ==========================================================

spark.sql("""

SELECT
'Bad' AS pipeline,
COUNT(*) AS price_mismatch

FROM fact_revenue_bad

WHERE ABS(price - product_price) > 0.01

UNION ALL

SELECT
'Good',
COUNT(*) AS price_mismatch

FROM fact_revenue_good

WHERE ABS(price - product_price) > 0.01

""").display()

# COMMAND ----------

# ==========================================================
# Query 5
# Duplicate Orders Comparison
# ==========================================================

spark.sql("""

SELECT
'Bad' AS pipeline,
COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_orders

FROM fact_revenue_bad

UNION ALL

SELECT
'Good' AS pipeline,
COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_orders

FROM fact_revenue_good

""").display()

# COMMAND ----------

# ==========================================================
# Query 6
# Revenue Trend by Order Date
# ==========================================================

spark.sql("""

SELECT
order_date,
ROUND(SUM(calculated_revenue),2) AS total_revenue

FROM fact_revenue_good

GROUP BY order_date

ORDER BY order_date

""").display()

# COMMAND ----------

spark.sql("SELECT * FROM fact_revenue_good LIMIT 5").display()

# COMMAND ----------

# ==========================================================
# Query 7
# Top 10 Customers by Revenue
# ==========================================================

spark.sql("""

SELECT
customer_id,
ROUND(SUM(calculated_revenue),2) AS revenue

FROM fact_revenue_good

GROUP BY customer_id

ORDER BY revenue DESC

LIMIT 10

""").display()

# COMMAND ----------

# ==========================================================
# Query 8
# Revenue by Payment Method
# ==========================================================

spark.sql("""

SELECT
payment_method,
ROUND(SUM(calculated_revenue),2) AS revenue

FROM fact_revenue_good

GROUP BY payment_method

ORDER BY revenue DESC

""").display()

# COMMAND ----------

# ==========================================================
# Query 9
# Revenue by Sales Channel
# ==========================================================

spark.sql("""

SELECT
channel,
ROUND(SUM(calculated_revenue),2) AS revenue

FROM fact_revenue_good

GROUP BY channel

ORDER BY revenue DESC

""").display()

# COMMAND ----------

# ==========================================================
# Query 10
# Revenue by Order Status
# ==========================================================

spark.sql("""

SELECT
order_status,
COUNT(*) AS total_orders,
ROUND(SUM(calculated_revenue),2) AS revenue

FROM fact_revenue_good

GROUP BY order_status

ORDER BY revenue DESC

""").display()

# COMMAND ----------

# ==========================================================
# Query 11
# Average Revenue Per Order
# ==========================================================

spark.sql("""

SELECT

ROUND(AVG(calculated_revenue),2) AS average_order_revenue

FROM fact_revenue_good

""").display()

# COMMAND ----------

from pyspark.sql.functions import count, sum, when, round, col

# COMMAND ----------

# ==========================================================
# Query 12
# Revenue Integrity Summary
# ==========================================================

summary = fact_good.agg(
    count("*").alias("total_orders"),
    sum("calculated_revenue").alias("total_revenue"),
    sum("payment_amount").alias("total_payment"),
    sum(
        when(col("payment_amount").isNull(), 1).otherwise(0)
    ).alias("missing_payments")
).withColumn(
    "accuracy_ratio",
    round(col("total_payment") / col("total_revenue"), 4)
)

display(summary)