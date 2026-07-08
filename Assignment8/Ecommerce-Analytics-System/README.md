# E-Commerce Order Analytics System

## Overview

This project is an end-to-end E-Commerce Order Analytics System built using Python, Pandas, SQLite, and SQL.

It generates realistic e-commerce datasets, cleans inconsistent data, validates relationships, performs advanced SQL analytics, and provides a command-line reporting tool for business insights.

---

## Features

- Generate realistic datasets
- Data cleaning using Pandas
- Email validation
- Referential integrity checks
- SQLite database integration
- SQL analytics using:
  - Joins
  - Aggregations
  - Window Functions
  - CTEs
  - Cohort Analysis
- Customer Segmentation
- CLI Reporting Tool
- Edge Case Testing

---

## Project Structure

```
Ecommerce-Analytics-System
│
├── Data
│   ├── Raw
│   └── Cleaned
│
├── Database
│   └── ecommerce.db
│
├── Scripts
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   └── report_cli.py
│
├── Sql
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   └── cohort_analysis.sql
│
├── Tests
│   └── test_edge_cases.py
│
├── Outputs
│   ├── Sample Reports
│   └── Screenshots
│
└── README.md
```

---

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Faker

---

## Steps to Run

### 1. Generate Dataset

```
python scripts/generate_data.py
```

### 2. Clean Dataset

```
python scripts/clean_data.py
```

### 3. Load Database

```
python scripts/load_database.py
```

### 4. Run CLI Report

```
python scripts/report_cli.py
```

### 5. Run Edge Case Tests

```
python Tests/test_edge_cases.py
```

---

## SQL Analysis

The project includes:

- Revenue Analysis
- Customer Segmentation
- Running Totals
- Product Ranking
- Cohort Analysis
- Year-over-Year Growth
- Cumulative Revenue
- Customer Retention

---

