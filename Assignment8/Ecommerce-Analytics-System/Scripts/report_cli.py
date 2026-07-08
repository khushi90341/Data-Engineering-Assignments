# ==========================================================
# File: report_cli.py
# Purpose:
# Generate E-Commerce Reports using SQLite Database
# ==========================================================

# Import required libraries
import sqlite3
from datetime import datetime, timedelta
# ==========================================================
# Connect to SQLite Database
# ==========================================================

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(BASE_DIR, "database", "ecommerce.db")

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()
# ==========================================================
# Take User Input
# ==========================================================

print("\n===== E-Commerce Analytics Report =====")

report_type = input(
    "Enter Report Type (daily/weekly/monthly): "
).lower()

start_date = input(
    "Enter Start Date (YYYY-MM-DD): "
)

end_date = input(
    "Enter End Date (YYYY-MM-DD): "
)
# ==========================================================
# Validate Report Type
# ==========================================================

if report_type not in ["daily", "weekly", "monthly"]:

    print("❌ Invalid Report Type!")

    connection.close()

    exit()

# Validate Date Format
try:

    datetime.strptime(start_date, "%Y-%m-%d")

    datetime.strptime(end_date, "%Y-%m-%d")

except ValueError:

    print("❌ Invalid Date Format!")

    connection.close()

    exit()
    # ==========================================================
# Calculate Previous Period
# ==========================================================

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

days = (end - start).days + 1

previous_end = start - timedelta(days=1)
previous_start = previous_end - timedelta(days=days - 1)

# ==========================================================
# Get Total Orders, Revenue and Unique Customers
# ==========================================================

query = """
SELECT

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS total_revenue,

    COUNT(DISTINCT o.customer_id) AS unique_customers

FROM orders o

JOIN order_items oi

ON o.order_id = oi.order_id

WHERE DATE(o.order_date)

BETWEEN ? AND ?;
"""

cursor.execute(query, (start_date, end_date))

summary = cursor.fetchone()

# ==========================================================
# Get Top 3 Products
# ==========================================================

query = """
SELECT

    p.product_name,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS revenue

FROM products p

JOIN order_items oi

ON p.product_id = oi.product_id

JOIN orders o

ON oi.order_id = o.order_id

WHERE DATE(o.order_date)

BETWEEN ? AND ?

GROUP BY p.product_name

ORDER BY revenue DESC

LIMIT 3;
"""

cursor.execute(query, (start_date, end_date))

top_products = cursor.fetchall()

# ==========================================================
# Previous Period Revenue
# ==========================================================

query = """
SELECT

ROUND(

SUM(

oi.quantity *

oi.unit_price *

(1 - oi.discount_percent / 100.0)

),

2

)

FROM orders o

JOIN order_items oi

ON o.order_id = oi.order_id

WHERE DATE(o.order_date)

BETWEEN ? AND ?;
"""

cursor.execute(

    query,

    (

        previous_start.strftime("%Y-%m-%d"),

        previous_end.strftime("%Y-%m-%d")

    )

)

previous_revenue = cursor.fetchone()[0]

if previous_revenue is None:
    previous_revenue = 0

    # ==========================================================
# Revenue Change Percentage
# ==========================================================

current_revenue = summary[1]

if current_revenue is None:
    current_revenue = 0

if previous_revenue > 0:

    revenue_change = (

        (current_revenue - previous_revenue)

        / previous_revenue

    ) * 100

else:

    revenue_change = 0

    # ==========================================================
# Display Report
# ==========================================================

print("\n")
print("=" * 50)
print("        E-COMMERCE ANALYTICS REPORT")
print("=" * 50)

print(f"Report Type       : {report_type.title()}")
print(f"Date Range        : {start_date} to {end_date}")

print("-" * 50)

print(f"Total Orders      : {summary[0]}")
print(f"Total Revenue     : ₹{current_revenue:.2f}")
print(f"Unique Customers  : {summary[2]}")

print("-" * 50)

print("Top 3 Products")

for product in top_products:

    print(f"{product[0]} : ₹{product[1]:.2f}")

print("-" * 50)

print(f"Revenue Change    : {revenue_change:.2f}%")

print("=" * 50)

# ==========================================================
# Close Database Connection
# ==========================================================

connection.close()

print("\n✅ Report Generated Successfully!")
