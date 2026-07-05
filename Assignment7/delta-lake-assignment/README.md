# Delta Lake MERGE Implementation

## Objective

This project demonstrates incremental data processing using Delta Lake on Azure Databricks.

---

## Technologies Used

- Azure Databricks
- Apache Spark
- Delta Lake
- Python (PySpark)

---

## Dataset

Superstore Dataset (Kaggle)

---

## Steps Performed

1. Loaded CSV dataset into Spark DataFrame.
2. Explored dataset.
3. Checked null values.
4. Removed duplicate records.
5. Handled missing values.
6. Renamed columns.
7. Converted numeric columns.
8. Created Delta Table.
9. Created Incremental Dataset.
10. Applied Delta MERGE operation.
11. Validated final results.
12. Displayed final dataset.

---

## Project Structure

```
delta-lake-assignment/
│
├── data/
├── notebooks/
├── screenshots/
├── report/
└── README.md
```

---

## Outcome

The MERGE operation successfully updated existing records and inserted new records into the Delta Table. Validation confirmed that the final dataset was updated correctly.
