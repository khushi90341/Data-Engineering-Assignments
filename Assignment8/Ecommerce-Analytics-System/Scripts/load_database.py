# ==========================================================
# File: load_database.py
# Purpose:
# Create SQLite database and load cleaned CSV files.
# ==========================================================

import sqlite3
import pandas as pd
import os

# ==========================================================
# Paths
# ==========================================================

DATABASE_PATH = "../database/ecommerce.db"

SCHEMA_PATH = "../sql/schema.sql"

CLEANED_DATA_PATH = "../data/cleaned"

# ==========================================================
# Connect Database
# ==========================================================

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

# ==========================================================
# Create Tables
# ==========================================================

with open(SCHEMA_PATH, "r") as file:

    schema = file.read()

cursor.executescript(schema)

connection.commit()

# ==========================================================
# Load Cleaned CSV Files
# ==========================================================

# Read cleaned datasets
customers_df = pd.read_csv(
    os.path.join(CLEANED_DATA_PATH, "customers_clean.csv")
)

products_df = pd.read_csv(
    os.path.join(CLEANED_DATA_PATH, "products_clean.csv")
)

orders_df = pd.read_csv(
    os.path.join(CLEANED_DATA_PATH, "orders_clean.csv")
)

order_items_df = pd.read_csv(
    os.path.join(CLEANED_DATA_PATH, "order_items_clean.csv")
)
# ==========================================================
# Insert Data into Database
# ==========================================================

customers_df.to_sql(
    "customers",
    connection,
    if_exists="append",
    index=False
)

products_df.to_sql(
    "products",
    connection,
    if_exists="append",
    index=False
)

orders_df.to_sql(
    "orders",
    connection,
    if_exists="append",
    index=False
)

order_items_df.to_sql(
    "order_items",
    connection,
    if_exists="append",
    index=False
)

# ==========================================================
# Verify Loaded Records
# ==========================================================

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

print("\nDatabase Summary")
print("=" * 30)

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table:<15}: {count} records")

    # ==========================================================
# Close Database Connection
# ==========================================================

connection.commit()

connection.close()

print("\n✅ SQLite Database Created Successfully!")