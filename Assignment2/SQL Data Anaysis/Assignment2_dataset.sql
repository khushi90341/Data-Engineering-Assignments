CREATE DATABASE superstore_analysis;
USE superstore_analysis;
USE superstore_analysis;

SHOW TABLES;

-- SECTION 1 DATA EXPLORATION
/* Q1. View first 10 records */
SELECT * FROM superstore LIMIT 10;

/* Q2. Total number of records */

SELECT COUNT(*) AS Total_Rows FROM superstore;

/* Q3. Table structure */

DESC superstore;

/* Q4. Distinct Categories */

SELECT DISTINCT Category FROM superstore;
-- SECTION 2 FILTERING
/* Q5. Orders from West Region */

SELECT * FROM superstore WHERE Region = 'West';
/* Q6. Technology Products */

SELECT * FROM superstore WHERE Category = 'Technology';

/* Q7. Sales greater than 1000 */

SELECT * FROM superstore WHERE Sales > 1000;
/* Q8. Furniture orders from East region */

SELECT * FROM superstore WHERE Category='Furniture' AND Region='East';

-- SECTION 3 AGGREGATION
/* Q9. Total Sales */

SELECT SUM(Sales) AS Total_Sales FROM superstore;
/* Q10. Average Sales */

SELECT AVG(Sales) AS Average_Sales FROM superstore;

/* Q11. Total Quantity Sold */

SELECT SUM(Quantity) AS Total_Quantity FROM superstore;

/* Q12. Total Profit */

SELECT SUM(Profit) AS Total_Profit FROM superstore;
-- SECTION 4 CATEGORY ANANLYSIS

/* Q13. Sales by Category */

SELECT Category, SUM(Sales) AS Total_Sales FROM superstore GROUP BY Category
ORDER BY Total_Sales DESC;
/* Q14. Profit by Category */

SELECT Category, SUM(Profit) AS Total_Profit FROM superstore
GROUP BY Category
ORDER BY Total_Profit DESC;

-- SECTION 5 TOP PRODUCTS
SELECT `Product Name`, SUM(Sales) AS Total_Sales FROM superstore
GROUP BY `Product Name`
ORDER BY Total_Sales DESC
LIMIT 10;
-- SECTION 6 TOP CONSUMERS
/* Q16. Top 10 Customers by Sales */

SELECT `Customer Name`, SUM(Sales) AS Total_Sales FROM superstore
GROUP BY `Customer Name`
ORDER BY Total_Sales DESC
LIMIT 10;
-- SECTION 7 REGION ANALYSIS
/* Q17. Sales by Region */

SELECT Region, SUM(Sales) AS Total_Sales FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC;

-- SECTION 8 BUSINESS USE CASE
/* Q18. Monthly Sales Trend */

SELECT
MONTH(STR_TO_DATE(`Order Date`, '%m/%d/%Y')) AS Month_No,
SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Month_No
ORDER BY Month_No;

/* Q19. Monthly Profit Trend */

SELECT
MONTH(STR_TO_DATE(`Order Date`, '%m/%d/%Y')) AS Month_No,
SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Month_No
ORDER BY Month_No;


/* Q24. Duplicate Order IDs */

SELECT
`Order ID`,
COUNT(*) AS Duplicate_Count
FROM superstore
GROUP BY `Order ID`
HAVING COUNT(*) > 1;

/*  business insights 
1. Technology category generates highest sales.

2. Some products are sold at a loss (negative profit),
   especially when high discounts are applied.

3. West region contributes the highest revenue.

4. Top customers contribute a significant portion of total sales.

5. Monthly sales show peak trends towards year-end.

6. High discounts negatively impact profitability. */

