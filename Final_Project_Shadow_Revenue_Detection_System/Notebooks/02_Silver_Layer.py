# Databricks notebook source
# MAGIC %md
# MAGIC ### # ==========================================================
# MAGIC ### # Project Name : Shadow Revenue Detection System
# MAGIC ### # Internship   : Celebal Technologies
# MAGIC ### # Layer        : Silver Layer
# MAGIC ### # Technology   : PySpark
# MAGIC ### 
# MAGIC ### # Objective:
# MAGIC ### # Clean raw data by removing duplicates, handling NULL
# MAGIC ### # values, converting data types and preparing data for
# MAGIC ### # Gold Layer analytics.
# MAGIC ### # ==========================================================

# COMMAND ----------

# ============================================
# Import Required Libraries
# ============================================

from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType

# COMMAND ----------

# ============================================
# Read Bronze Layer Datasets
# ============================================

customers_df = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/customers"
)

orders_df = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/orders"
)

payments_df = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/payments"
)

products_df = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/products"
)

# COMMAND ----------

display(customers_df)

display(orders_df)

display(payments_df)

display(products_df)

# COMMAND ----------

# ============================================
# BAD PIPELINE
# No Cleaning
# No Deduplication
# ============================================

silver_orders_bad = orders_df

silver_payments_bad = payments_df

silver_products_bad = products_df.filter(col("is_current") == 1)

silver_customers_bad = customers_df

# COMMAND ----------

silver_orders_bad.createOrReplaceTempView("silver_orders_bad")

silver_payments_bad.createOrReplaceTempView("silver_payments_bad")

silver_products_bad.createOrReplaceTempView("silver_products_bad")

silver_customers_bad.createOrReplaceTempView("silver_customers_bad")

# COMMAND ----------

# ============================================
# Find Duplicate Order IDs
# ============================================

duplicate_orders = (
    orders_df.groupBy("order_id")
             .count()
             .filter(col("count") > 1)
)

display(duplicate_orders)

# COMMAND ----------

# ============================================
# Window Specification
# ============================================

window_spec = (
    Window.partitionBy("order_id")
          .orderBy(col("order_date").desc())
)

# COMMAND ----------

# ============================================
# Remove Duplicate Orders
# ============================================

orders_dedup = (
    orders_df
    .withColumn("rn", row_number().over(window_spec))
    .filter(col("rn") == 1)
    .drop("rn")
)

display(orders_dedup)

# COMMAND ----------

# ============================================
# Save Bronze Layer as Parquet Files
# ============================================

customers_df.write.mode("overwrite").parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/customers"
)

orders_df.write.mode("overwrite").parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/orders"
)

payments_df.write.mode("overwrite").parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/payments"
)

products_df.write.mode("overwrite").parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/products"
)

print("✅ Bronze Layer Created Successfully!")

# COMMAND ----------

bronze_orders = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/orders"
)

display(bronze_orders)

# COMMAND ----------

# ============================================
# Clean Customers Dataset
# ============================================

# Remove duplicate customer records
customers_clean = customers_df.dropDuplicates()

display(customers_clean)

# COMMAND ----------

# ============================================
# Convert Monetary Columns to Decimal
# ============================================

orders_clean = (
    orders_dedup
    .withColumn("price", col("price").cast(DecimalType(10,4)))
    .withColumn("order_date", to_date(col("order_date")))
)

payments_clean = (
    payments_df
    .withColumn("payment_amount", col("payment_amount").cast(DecimalType(10,4)))
    .withColumn("payment_date", to_date(col("payment_date")))
)

products_clean = (
    products_df
    .withColumn("price", col("price").cast(DecimalType(10,4)))
    .withColumn("effective_date", to_date(col("effective_date")))
    .withColumn("end_date", to_date(col("end_date")))
)

# COMMAND ----------

# ============================================
# Remove NULL Values
# ============================================

orders_clean = orders_clean.filter(col("order_id").isNotNull())

payments_clean = payments_clean.filter(col("order_id").isNotNull())

customers_clean = customers_df.filter(col("customer_id").isNotNull())

products_clean = products_clean.filter(col("product_id").isNotNull())

# COMMAND ----------

display(orders_clean)

display(payments_clean)

display(products_clean)

display(customers_clean)

# COMMAND ----------

# ============================================
# Save Silver Layer
# ============================================

orders_clean.write.mode("overwrite").parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/orders"
)

payments_clean.write.mode("overwrite").parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/payments"
)

products_clean.write.mode("overwrite").parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/products"
)

customers_clean.write.mode("overwrite").parquet(
"/Volumes/workspace/default/shadow_revenue_data/silver/customers"
)

print("✅ Silver Layer Created Successfully!")

# COMMAND ----------

# ============================================
# Read Silver Layer
# ============================================

silver_orders = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/silver/orders"
)

display(silver_orders)

silver_orders.printSchema()

# COMMAND ----------

orders_clean.createOrReplaceTempView("silver_orders_good")

payments_clean.createOrReplaceTempView("silver_payments_good")

products_clean.createOrReplaceTempView("silver_products_good")

customers_clean.createOrReplaceTempView("silver_customers_good")

# COMMAND ----------

print("Orders :", orders_clean.count())

print("Payments :", payments_clean.count())

print("Products :", products_clean.count())

print("Customers :", customers_clean.count())