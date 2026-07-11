# Shadow Revenue Detection System

## Project Overview

The Shadow Revenue Detection System is an end-to-end Data Engineering project developed using PySpark, Spark SQL, Databricks, and the Medallion Architecture. The project identifies hidden financial leakages in retail transaction data by processing raw datasets through Bronze, Silver, and Gold layers.

The system detects key revenue anomalies such as missing payments, orphan payments, duplicate orders, price mismatches, and revenue differences. It also compares a naive (Bad) pipeline with a production-grade (Good) pipeline to demonstrate the importance of data quality and proper engineering practices.

---

## Technologies Used

- PySpark
- Spark SQL
- Databricks
- Python
- Delta/Parquet Storage
- Medallion Architecture

---

## Project Architecture

Bronze Layer
- Read raw CSV datasets
- Store raw data as Parquet files

Silver Layer
- Remove duplicate records
- Handle null values
- Convert monetary columns to DecimalType
- Parse date columns
- Prepare clean datasets

Gold Layer
- Join datasets
- Detect missing payments
- Detect orphan payments
- Detect price mismatches
- Calculate KPIs
- Build Revenue Integrity Report

---

## Datasets

The project uses four datasets:

- Customers
- Orders
- Payments
- Products

---

## Revenue Anomalies Detected

- Missing Payments
- Orphan Payments
- Duplicate Orders
- Price Mismatches
- Revenue Difference

---

## KPIs Generated

- Total Revenue
- Total Payment
- Revenue Difference
- Accuracy Ratio
- Missing Payments Count
- Orphan Payments Count

---

## Spark SQL Analytics

The project includes multiple Spark SQL queries for:

- KPI Comparison
- Missing Payments
- Price Mismatch Analysis
- Duplicate Orders
- Revenue Trend
- Revenue by Channel
- Revenue by Payment Method
- Revenue by Order Status
- Customer Revenue Analysis

---

## Dashboard

The dashboard provides visualizations for:

- Revenue Comparison
- KPI Summary
- Revenue Trend
- Payment Method Distribution
- Revenue by Channel

---

## Folder Structure

```
Final_Project_Shadow_Revenue_Detection_System/
│
├── 01_Bronze_Layer.py
├── 02_Silver_Layer.py
├── 03_Gold_Layer.py
├── 04_Spark_SQL_Analytics.py
├── 05_Dashboard.py
└── README.md
```

---

## Learning Outcomes

- Medallion Architecture
- Data Cleaning using PySpark
- Spark SQL Analytics
- Window Functions
- LEFT JOIN and LEFT ANTI JOIN
- KPI Computation
- Dashboard Development
- Revenue Integrity Analysis

---

## Author

Khushi Arora

Celebal Technologies Internship Project