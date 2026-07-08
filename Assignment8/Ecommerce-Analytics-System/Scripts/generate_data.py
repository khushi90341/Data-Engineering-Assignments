# ==========================================================
# File: generate_data.py
# Purpose:
# Generate realistic e-commerce datasets with intentional
# inconsistencies for analytics.
# ==========================================================

# Import required libraries
import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

# Initialize Faker object
fake = Faker()

# Set random seed so that generated data remains the same
# every time the script is executed (helps in debugging)
random.seed(42)
Faker.seed(42)

# ==========================================================
# Project Constants
# ==========================================================

# Number of records to generate
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 500
NUM_ORDER_ITEMS = 1000

# Customer Types
CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

# Order Status
ORDER_STATUS = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

# Regions
REGIONS = [
    "North",
    "South",
    "East",
    "West"
]

# Product Categories and Subcategories
CATEGORIES = {
    "Electronics": [
        "Mobile",
        "Laptop",
        "Headphones",
        "Camera"
    ],
    "Clothing": [
        "Shirt",
        "Jeans",
        "Shoes",
        "Jacket"
    ],
    "Home": [
        "Furniture",
        "Kitchen",
        "Decor",
        "Lighting"
    ],
    "Books": [
        "Fiction",
        "Education",
        "Biography",
        "Comics"
    ]
}

# ==========================================================
# Create Raw Data Directory
# ==========================================================

# Path where generated CSV files will be stored
RAW_DATA_PATH = "../data/raw"

# Create the directory if it doesn't already exist
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# ==========================================================
# Function to Generate Customers Data
# ==========================================================

def generate_customers():
    """
    Generates customer data with intentional invalid emails.
    Returns a Pandas DataFrame.
    """

    # List to store customer records
    customers = []

    # Loop to generate customer records
    for customer_id in range(1, NUM_CUSTOMERS + 1):

        # Generate customer details
        customer_name = fake.name()
        email = fake.email()
        registration_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        customer_type = random.choice(CUSTOMER_TYPES)

        # --------------------------------------------------
        # Introduce 2% invalid emails
        # --------------------------------------------------
        if random.random() < 0.02:

            # Randomly create different types of invalid emails
            invalid_email_type = random.choice([1, 2])

            if invalid_email_type == 1:
                # Missing '@'
                email = email.replace("@", "")

            else:
                # Missing domain
                email = email.split("@")[0] + "@"

        # Append record
        customers.append({
            "customer_id": customer_id,
            "customer_name": customer_name,
            "email": email,
            "registration_date": registration_date,
            "customer_type": customer_type
        })

    # Convert list into DataFrame
    customers_df = pd.DataFrame(customers)

    return customers_df

# ==========================================================
# Function to Generate Products Data
# ==========================================================

def generate_products():
    """
    Generates product data with intentional formatting issues.
    Returns a Pandas DataFrame.
    """

    # List to store product records
    products = []

    # Generate product records
    for product_id in range(1, NUM_PRODUCTS + 1):

        # Select random category
        category = random.choice(list(CATEGORIES.keys()))

        # Select matching subcategory
        subcategory = random.choice(CATEGORIES[category])

        # Create product name
        product_name = f"{fake.word().capitalize()} {subcategory}"

        # --------------------------------------------------
        # Introduce formatting issues
        # --------------------------------------------------

        # Extra spaces (5%)
        if random.random() < 0.05:
            product_name = "   " + product_name + "   "

        # Mixed case (5%)
        if random.random() < 0.05:
            product_name = product_name.swapcase()

        # Random cost price
        cost_price = round(random.uniform(100, 5000), 2)

        # Append record
        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": cost_price
        })

    # Convert list into DataFrame
    products_df = pd.DataFrame(products)

    return products_df

# ==========================================================
# Function to Generate Orders Data
# ==========================================================

def generate_orders():
    """
    Generates orders data with intentional issues:
    - 5% NULL customer_id
    - Some incorrect date formats
    """

    # List to store orders
    orders = []

    # Generate order records
    for order_id in range(1, NUM_ORDERS + 1):

        # -----------------------------------------------
        # 5% NULL customer_id
        # -----------------------------------------------
        if random.random() < 0.05:
            customer_id = None
        else:
            customer_id = random.randint(1, NUM_CUSTOMERS)

        # Generate random order date
        order_datetime = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        # -----------------------------------------------
        # Introduce wrong date format (5%)
        # -----------------------------------------------
        if random.random() < 0.05:
            order_date = order_datetime.strftime("%d-%m-%Y %H:%M:%S")
        else:
            order_date = order_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Random region
        region = random.choice(REGIONS)

        # Random status
        status = random.choice(ORDER_STATUS)

        # Append record
        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "region_code": region,
            "status": status
        })

    # Convert list into DataFrame
    orders_df = pd.DataFrame(orders)

    return orders_df

# ==========================================================
# Function to Generate Order Items Data
# ==========================================================

def generate_order_items():
    """
    Generates order items data with intentional issues:
    - 3% negative quantity
    - Valid order_id references
    - Valid product_id references
    """

    # List to store order items
    order_items = []

    # Generate order item records
    for order_item_id in range(1, NUM_ORDER_ITEMS + 1):

        # Select existing order and product IDs
        order_id = random.randint(1, NUM_ORDERS)
        product_id = random.randint(1, NUM_PRODUCTS)

        # Generate quantity
        quantity = random.randint(1, 5)

        # -----------------------------------------------
        # Introduce negative quantity (3%)
        # -----------------------------------------------
        if random.random() < 0.03:
            quantity = -quantity

        # Unit price
        unit_price = round(random.uniform(200, 8000), 2)

        # Discount percentage
        discount_percent = round(random.uniform(0, 100), 2)

        # Append record
        order_items.append({
            "order_item_id": order_item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_percent": discount_percent
        })

    # Convert list into DataFrame
    order_items_df = pd.DataFrame(order_items)

    return order_items_df

# ==========================================================
# Main Function
# ==========================================================

def main():
    """
    Main function to generate datasets.
    """

    # Generate customers data
    customers_df = generate_customers()

    # Save customers data to CSV
    customers_df.to_csv(
        os.path.join(RAW_DATA_PATH, "customers.csv"),
        index=False
    )

    print("✅ customers.csv generated successfully!")

        # Generate products data
    products_df = generate_products()

    # Save products data
    products_df.to_csv(
        os.path.join(RAW_DATA_PATH, "products.csv"),
        index=False
    )

    print("✅ products.csv generated successfully!")

        # Generate orders data
    orders_df = generate_orders()

    # Save orders data
    orders_df.to_csv(
        os.path.join(RAW_DATA_PATH, "orders.csv"),
        index=False
    )

    print("✅ orders.csv generated successfully!")

        # Generate order items data
    order_items_df = generate_order_items()

    # Save order items data
    order_items_df.to_csv(
        os.path.join(RAW_DATA_PATH, "order_items.csv"),
        index=False
    )

    print("✅ order_items.csv generated successfully!")


# ==========================================================
# Program Entry Point
# ==========================================================

if __name__ == "__main__":
    main()
