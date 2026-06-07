# Week 3 - SQL Advanced Analysis

## Objective

Analyze Superstore sales data using SQL Subqueries, CTEs, and Window Functions to solve business problems and generate insights.

---

## Dataset

Sample - Superstore Dataset

---

## Tools Used

* MySQL Workbench
* SQL
* Visual Studio Code
* GitHub

---

## Tasks Performed

### Data Setup

* Imported Superstore dataset into `superstore_raw`
* Created `customers`, `orders`, and `products` tables
* Inserted data using `SELECT DISTINCT`

### SQL Concepts Used

* Subqueries
* Common Table Expressions (CTEs)
* Window Functions
* JOIN Operations
* Ranking Functions

### Business Queries Solved

* Orders above average sales
* Highest sales order per customer
* Total sales per customer
* Customers above average sales
* Customer ranking using RANK()
* Row numbering using ROW_NUMBER()
* Top 5 customers
* Bottom 5 customers
* Customers with only one order

### Final Combined Query

Displayed:

* Customer Name
* Total Sales
* Customer Rank

using JOIN + CTE + Window Functions.

---

## Key Insights

1. A small number of customers generate a significant portion of total sales.
2. Several customers place only one order, highlighting retention opportunities.
3. Sales performance varies greatly across customers.
4. Top customers can be targeted for loyalty and reward programs.

---

## Project Structure

dataset/
screenshots/
SQL Scripts/
Insights.txt
README.md
