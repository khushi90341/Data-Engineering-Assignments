# ==========================================================
# File: clean_data.py
# Purpose:
# Clean and validate raw e-commerce datasets.
# ==========================================================

# Import required libraries
import os
import re
import pandas as pd

# ==========================================================
# Define File Paths
# ==========================================================

RAW_DATA_PATH = "../data/raw"
CLEANED_DATA_PATH = "../data/cleaned"

# Create cleaned folder if it doesn't exist
os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

# ==========================================================
# Load Raw CSV Files
# ==========================================================

customers_df = pd.read_csv(
    os.path.join(RAW_DATA_PATH, "customers.csv")
)

products_df = pd.read_csv(
    os.path.join(RAW_DATA_PATH, "products.csv")
)

orders_df = pd.read_csv(
    os.path.join(RAW_DATA_PATH, "orders.csv")
)

order_items_df = pd.read_csv(
    os.path.join(RAW_DATA_PATH, "order_items.csv")
)
# ==========================================================
# Store All Issues Found During Cleaning
# ==========================================================

issues = []

# ==========================================================
# Function: Clean Orders Data
# ==========================================================

def clean_orders():
    """
    Cleans the orders dataset by:
    1. Fixing incorrect date formats
    2. Handling NULL customer IDs
    """

    global orders_df

    # -------------------------------
    # Handle NULL customer_id
    # -------------------------------
    null_count = orders_df["customer_id"].isnull().sum()

    if null_count > 0:
        issues.append(f"NULL customer_id found: {null_count}")

        # Replace NULL values with -1
        orders_df["customer_id"] = orders_df["customer_id"].fillna(-1)

    # Convert customer_id to integer
    orders_df["customer_id"] = orders_df["customer_id"].astype(int)

    # -------------------------------
    # Fix Incorrect Date Formats
    # -------------------------------
    corrected_dates = []

    for date in orders_df["order_date"]:

        try:
            # Correct Format
            parsed_date = pd.to_datetime(
                date,
                format="%Y-%m-%d %H:%M:%S"
            )

        except:

            try:
                # Wrong Format
                parsed_date = pd.to_datetime(
                    date,
                    format="%d-%m-%Y %H:%M:%S"
                )

                issues.append(
                    f"Incorrect date format corrected: {date}"
                )

            except:
                parsed_date = pd.NaT

                issues.append(
                    f"Invalid date removed: {date}"
                )

        corrected_dates.append(parsed_date)

    # Replace old dates
    orders_df["order_date"] = corrected_dates

    # Save cleaned orders
orders_df.to_csv(
    os.path.join(CLEANED_DATA_PATH, "orders_clean.csv"),
    index=False
)
# ==========================================================
# Function: Clean Products Data
# ==========================================================

def clean_products():
    """
    Cleans product names by:
    1. Removing extra spaces
    2. Converting names to Title Case
    """

    global products_df

    corrected_count = 0

    # Loop through all product names
    for index in products_df.index:

        original_name = products_df.loc[index, "product_name"]

        # Remove extra spaces
        cleaned_name = original_name.strip()

        # Convert to Title Case
        cleaned_name = cleaned_name.title()

        # Check if any change was made
        if original_name != cleaned_name:
            corrected_count += 1

        # Update DataFrame
        products_df.loc[index, "product_name"] = cleaned_name

    # Store issue count
    issues.append(
        f"Product names corrected: {corrected_count}"
    )

    # ==========================================================
# Function: Validate Customer Emails
# ==========================================================

def validate_emails():
    """
    Returns list of customer IDs having invalid email addresses.
    """

    invalid_customers = []

    # Email pattern
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    # Check every email
    for index in customers_df.index:

        email = str(customers_df.loc[index, "email"])

        if not re.match(email_pattern, email):

            customer_id = customers_df.loc[index, "customer_id"]

            invalid_customers.append(customer_id)

    issues.append(
        f"Invalid Emails Found: {len(invalid_customers)}"
    )

    return invalid_customers
# ==========================================================
# Function: Check Referential Integrity
# ==========================================================

def check_referential_integrity():
    """
    Checks whether every order_id in order_items
    exists in orders table.
    """

    # Get all valid order IDs
    valid_order_ids = set(orders_df["order_id"])

    # Find invalid order references
    invalid_orders = order_items_df[
        ~order_items_df["order_id"].isin(valid_order_ids)
    ]

    # Store issue count
    issues.append(
        f"Invalid Order References: {len(invalid_orders)}"
    )

    return invalid_orders
# ==========================================================
# Main Function
# ==========================================================

def main():

    # Clean datasets
    clean_orders()
    clean_products()

    # Validate data
    invalid_emails = validate_emails()
    invalid_orders = check_referential_integrity()

    # Save cleaned datasets
    customers_df.to_csv(
        os.path.join(CLEANED_DATA_PATH, "customers_clean.csv"),
        index=False
    )

    products_df.to_csv(
        os.path.join(CLEANED_DATA_PATH, "products_clean.csv"),
        index=False
    )

    orders_df.to_csv(
        os.path.join(CLEANED_DATA_PATH, "orders_clean.csv"),
        index=False
    )

    order_items_df.to_csv(
        os.path.join(CLEANED_DATA_PATH, "order_items_clean.csv"),
        index=False
    )

    # Save Issues Report
    with open(
        os.path.join(CLEANED_DATA_PATH, "issues_report.txt"),
        "w"
    ) as report:

        report.write("E-Commerce Data Cleaning Report\n")
        report.write("=" * 40 + "\n\n")

        for issue in issues:
            report.write(issue + "\n")

        report.write("\n")

        report.write(
            f"Invalid Customer IDs (Email): {invalid_emails}\n\n"
        )

        report.write(
            "Invalid Order References:\n"
        )

        report.write(
            invalid_orders.to_string(index=False)
        )

    print("✅ Data Cleaning Completed Successfully!")

    # ==========================================================
# Program Entry Point
# ==========================================================

if __name__ == "__main__":
    main()