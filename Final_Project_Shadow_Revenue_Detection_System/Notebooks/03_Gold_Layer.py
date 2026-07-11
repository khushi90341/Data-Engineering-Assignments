# Databricks notebook source
# MAGIC %md
# MAGIC ### # ==========================================================
# MAGIC ### # Project Name : Shadow Revenue Detection System
# MAGIC ### # Layer        : Gold Layer
# MAGIC ### # Objective    :
# MAGIC ### # Build analytical fact table and detect revenue anomalies
# MAGIC ### # ==========================================================

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

orders = spark.read.parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/orders"
)

payments = spark.read.parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/payments"
)

products = spark.read.parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/products"
)

customers = spark.read.parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/customers"
)

# COMMAND ----------

# ==========================================================
# Step 1: Handle SCD Type 2 Product Data
# ----------------------------------------------------------
# Keep only the current (active) product records from the
# product catalog. This ensures that revenue is calculated
# using the latest product price instead of historical prices.
# ==========================================================

product_scd = (
    products
    .filter(col("is_current") == 1)
    .select(
        "product_id",
        col("price").alias("product_price")
    )
)

# COMMAND ----------

fact_revenue_good = (
    orders.alias("o")
    .join(product_scd.alias("p"), "product_id", "left")
    .join(payments.alias("pay"), "order_id", "left")
    .join(customers.alias("c"), "customer_id", "left")
    .withColumn(
        "calculated_revenue",
        col("quantity") * col("product_price")
    )
)

display(fact_revenue_good)

# COMMAND ----------

# ==========================================================
# Step 3: Detect Missing Payments
# ----------------------------------------------------------
# Orders that do not have a corresponding payment record
# are identified using NULL values after a LEFT JOIN.
# These indicate expected revenue that has not been received.
# ==========================================================

missing_payments = fact_revenue_good.filter(
    col("payment_amount").isNull()
)
missing_payments = fact_revenue_good.filter(
    col("payment_amount").isNull()
)

display(missing_payments)

# COMMAND ----------

orphan_payments = (
    payments.join(
        orders,
        "order_id",
        "left_anti"
    )
)

display(orphan_payments)

# COMMAND ----------

price_mismatch = fact_revenue_good.filter(
    col("price") != col("product_price")
)

display(price_mismatch)

# COMMAND ----------

kpi_df = (
    fact_revenue_good
    .agg(
        sum("calculated_revenue").alias("total_revenue"),
        sum("payment_amount").alias("total_payment")
    )
    .withColumn(
        "revenue_difference",
        col("total_revenue") - col("total_payment")
    )
    .withColumn(
        "accuracy_ratio",
        round(
            col("total_payment") /
            col("total_revenue"),
            4
        )
    )
)

display(kpi_df)

# COMMAND ----------

fact_revenue_good.write.mode("overwrite").parquet(
"/Volumes/workspace/default/shadow_revenue_data/gold/fact_revenue_good"
)

kpi_df.write.mode("overwrite").parquet(
"/Volumes/workspace/default/shadow_revenue_data/gold/kpi_revenue_good"
)

print("✅ Gold Layer Created Successfully!")

# COMMAND ----------

fact_revenue_good.createOrReplaceTempView(
"fact_revenue_good"
)

kpi_df.createOrReplaceTempView(
"kpi_revenue_good"
)

# COMMAND ----------

# ==========================================================
# Step 6: Read Bronze Layer Data for Bad Pipeline
# ----------------------------------------------------------
# Read the raw Bronze data to build the Bad Pipeline.
# ==========================================================

orders_bad = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/orders"
)

payments_bad = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/payments"
)

products_bad = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/products"
)

customers_bad = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/customers"
)

print("✅ Bronze data loaded for Bad Pipeline")

# COMMAND ----------

# ==========================================================
# Step 7: Keep Current Product Records
# ==========================================================

from pyspark.sql.functions import col

products_bad_current = (
    products_bad
    .filter(col("is_current") == 1)
    .select(
        "product_id",
        col("price").alias("product_price")
    )
)

display(products_bad_current)

# COMMAND ----------

# ==========================================================
# Step 8: Create Bad Revenue Fact Table
# ----------------------------------------------------------
# The Bad Pipeline performs joins on raw data without
# deduplication or proper data quality checks.
# Revenue is calculated using the order price, which may
# contain duplicates and incorrect prices.
# ==========================================================

fact_revenue_bad = (
    orders_bad.alias("o")
    .join(
        products_bad_current.alias("p"),
        "product_id",
        "left"
    )
    .join(
        payments_bad.alias("pay"),
        "order_id",
        "left"
    )
    .join(
        customers_bad.alias("c"),
        "customer_id",
        "left"
    )
    .withColumn(
        "calculated_revenue",
        col("quantity") * col("price")
    )
)

display(fact_revenue_bad)

# COMMAND ----------

# ==========================================================
# Step 9: Calculate KPIs for Bad Pipeline
# ----------------------------------------------------------
# Calculate the key business metrics for the Bad Pipeline.
# These KPIs will later be compared with the Good Pipeline.
# ==========================================================

from pyspark.sql.functions import sum, round

kpi_bad = (
    fact_revenue_bad
    .agg(
        sum("calculated_revenue").alias("total_revenue"),
        sum("payment_amount").alias("total_payment")
    )
    .withColumn(
        "revenue_difference",
        col("total_revenue") - col("total_payment")
    )
    .withColumn(
        "accuracy_ratio",
        round(
            col("total_payment") / col("total_revenue"),
            4
        )
    )
)

display(kpi_bad)

# COMMAND ----------

# ==========================================================
# Step 10: Save Bad Pipeline Outputs
# ----------------------------------------------------------
# Save the Bad Pipeline Fact Table and KPI table into
# the Gold Layer for comparison with the Good Pipeline.
# ==========================================================

fact_revenue_bad.write.mode("overwrite").parquet(
    "/Volumes/workspace/default/shadow_revenue_data/gold/fact_revenue_bad"
)

kpi_bad.write.mode("overwrite").parquet(
    "/Volumes/workspace/default/shadow_revenue_data/gold/kpi_revenue_bad"
)

print("✅ Bad Pipeline Saved Successfully!")

# COMMAND ----------

# ==========================================================
# Save Gold Tables
# ==========================================================

fact_revenue_good.write.mode("overwrite").saveAsTable("fact_revenue_good")

fact_revenue_bad.write.mode("overwrite").saveAsTable("fact_revenue_bad")

print("Gold tables saved successfully!")

# COMMAND ----------

# ==========================================================
# Verify Gold Layer
# ==========================================================

gold_good = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/gold/fact_revenue_good"
)

display(gold_good)

gold_good.printSchema()