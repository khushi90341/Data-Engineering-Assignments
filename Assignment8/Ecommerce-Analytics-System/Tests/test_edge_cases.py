# ==========================================================
# File: test_edge_cases.py
# Purpose:
# Test important edge cases for the E-Commerce Analytics System
# ==========================================================

import pandas as pd
from datetime import datetime
# ==========================================================
# Test 1: Invalid Order ID
# ==========================================================

def test_invalid_order_id():

    print("\nTest 1 : Invalid Order ID")

    orders = pd.DataFrame({

        "order_id":[1,2,3]

    })

    order_items = pd.DataFrame({

        "order_id":[1,2,5]

    })

    invalid = order_items[
        ~order_items["order_id"].isin(orders["order_id"])
    ]

    print(invalid)

    # ==========================================================
# Test 2 : Discount Greater Than 100
# ==========================================================

def test_discount():

    print("\nTest 2 : Discount >100")

    discount = 120

    if discount >100:

        print("Invalid Discount")

    else:

        print("Valid Discount")

        # ==========================================================
# Test 3 : Quantity Zero
# ==========================================================

def test_zero_quantity():

    print("\nTest 3 : Quantity =0")

    quantity=0

    if quantity<=0:

        print("Invalid Quantity")

    else:

        print("Valid Quantity")

        # ==========================================================
# Test 4 : Future Order Date
# ==========================================================

def test_future_date():

    print("\nTest 4 : Future Date")

    future=datetime(2030,1,1)

    if future>datetime.now():

        print("Future Date Found")

    else:

        print("Valid Date")

        # ==========================================================
# Main Function
# ==========================================================

if __name__=="__main__":

    test_invalid_order_id()

    test_discount()

    test_zero_quantity()

    test_future_date()