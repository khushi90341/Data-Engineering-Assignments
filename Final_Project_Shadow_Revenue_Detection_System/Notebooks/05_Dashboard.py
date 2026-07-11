# Databricks notebook source
# ==========================================================
# Import Required Libraries
# ==========================================================

from pyspark.sql.functions import *

# COMMAND ----------

# ==========================================================
# Load Gold Layer Tables
# ==========================================================

fact_revenue_good = spark.table("fact_revenue_good")
fact_revenue_bad = spark.table("fact_revenue_bad")

# COMMAND ----------

# ==========================================================
# Total Revenue Comparison
# ==========================================================

display(

fact_revenue_good.groupBy()
.agg(sum("calculated_revenue").alias("Revenue"))
.withColumn("Pipeline", lit("Good"))

.union(

fact_revenue_bad.groupBy()
.agg(sum("calculated_revenue").alias("Revenue"))
.withColumn("Pipeline", lit("Bad"))

)

)

# COMMAND ----------

# ==========================================================
# Dashboard 1
# KPI Summary
# ==========================================================

display(

fact_revenue_good.select(
"calculated_revenue",
"payment_amount"
)

)

# COMMAND ----------

# ==========================================================
# Dashboard 2
# Revenue Trend
# ==========================================================

display(

fact_revenue_good.groupBy("order_date")
.agg(
sum("calculated_revenue").alias("Total Revenue")
)
.orderBy("order_date")

)

# COMMAND ----------

# ==========================================================
# Dashboard 3
# Payment Method Distribution
# ==========================================================

display(

fact_revenue_good.groupBy("payment_method")
.count()

)

# COMMAND ----------

# ==========================================================
# Dashboard 4
# Revenue by Order Status
# ==========================================================

display(

fact_revenue_good.groupBy("order_status")
.agg(
sum("calculated_revenue").alias("Revenue")
)

)

# COMMAND ----------

# ==========================================================
# Dashboard 5
# Revenue by Channel
# ==========================================================

display(

fact_revenue_good.groupBy("channel")
.agg(
sum("calculated_revenue").alias("Revenue")
)

)

# COMMAND ----------

spark.sql("SHOW TABLES").display()