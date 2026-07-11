# Databricks notebook source
# MAGIC %md
# MAGIC ### ## # ======================================
# MAGIC ### ## # Project Name : Shadow Revenue Detection System
# MAGIC ### ## # Internship   : Celebal Technologies
# MAGIC ### ## # Layer        : Bronze Layer
# MAGIC ### ## # Technology   : PySpark
# MAGIC ### ## # Objective:
# MAGIC ### ## # Read raw retail datasets and store them in Bronze Layer
# MAGIC ### ## # without applying any transformations.
# MAGIC ### # ==========================================================

# COMMAND ----------

# Import required libraries

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# ============================================
# Read Customers Dataset
# ============================================

customers_df = (
    spark.read
         .option("header", True)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/shadow_revenue_data/customers.csv")
)

display(customers_df)

# COMMAND ----------

# ============================================
# Read Orders Dataset
# ============================================

orders_df = (
    spark.read
         .option("header", True)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/shadow_revenue_data/orders.csv")
)

display(orders_df)

# COMMAND ----------

# ============================================
# Read Payments Dataset
# ============================================

payments_df = (
    spark.read
         .option("header", True)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/shadow_revenue_data/payments.csv")
)

display(payments_df)

# COMMAND ----------

# ============================================
# Read Products Dataset
# ============================================

products_df = (
    spark.read
         .option("header", True)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/shadow_revenue_data/products.csv")
)

display(products_df)

# COMMAND ----------

# ============================================
# Count Records in Each Dataset
# ============================================

print("Customers :", customers_df.count())

print("Orders :", orders_df.count())

print("Payments :", payments_df.count())

print("Products :", products_df.count())

# COMMAND ----------

# ============================================
# Print Schema of Each Dataset
# ============================================

print("Customers Schema")
customers_df.printSchema()

print("Orders Schema")
orders_df.printSchema()

print("Payments Schema")
payments_df.printSchema()

print("Products Schema")
products_df.printSchema()

# COMMAND ----------

# ============================================
# Save Bronze Layer as Parquet Files
# ============================================

customers_df.write.mode("overwrite").parquet("/Volumes/workspace/default/shadow_revenue_data/bronze/customers")

orders_df.write.mode("overwrite").parquet("/Volumes/workspace/default/shadow_revenue_data/bronze/orders")

payments_df.write.mode("overwrite").parquet("/Volumes/workspace/default/shadow_revenue_data/bronze/payments")

products_df.write.mode("overwrite").parquet("/Volumes/workspace/default/shadow_revenue_data/bronze/products")

# COMMAND ----------

# ============================================
# Read Bronze Orders Dataset
# ============================================

bronze_orders = spark.read.parquet(
    "/Volumes/workspace/default/shadow_revenue_data/bronze/orders"
)

display(bronze_orders)