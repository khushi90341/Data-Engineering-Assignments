Week 5 - Insights
Key Learnings
Apache Spark is faster than MapReduce because it uses in-memory processing instead of repeatedly reading and writing data to disk.
Spark DataFrames are immutable, meaning every transformation creates a new DataFrame.
Data cleaning improves data quality by removing duplicates, handling null values, and fixing inconsistent records.
Filtering helps extract only relevant records based on conditions such as region, age, or subscription type.
Aggregation functions like count(), sum(), avg(), min(), and max() help generate useful business insights.
groupBy() operations trigger shuffle, which redistributes data across partitions and is considered a wide transformation.
Schema modifications such as casting data types and renaming columns improve data consistency and analysis accuracy.
Final Pipeline Summary

The final Spark pipeline performed:

Duplicate removal
Null value handling
Data filtering
Aggregation using groupBy()
Revenue calculation by store_id
Conclusion

This assignment demonstrated Spark DataFrame operations for data cleaning, transformation, aggregation, schema handling, and building a complete ETL-style processing pipeline. Spark provides efficient and scalable processing for large datasets.