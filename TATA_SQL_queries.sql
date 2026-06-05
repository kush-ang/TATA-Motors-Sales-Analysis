create database tata_motors;
-- use tata_motors;

-- Query 1: Top Countries by Average Sale Price

SELECT country, 
       ROUND(AVG(average_sale_price), 2) AS avg_price
FROM tata_sales
GROUP BY country
ORDER BY avg_price DESC;

-- Query 2 : Discount Leakage Analysis

SELECT discount_reason,
	 ROUND(AVG(dealer_discount_pct),2) AS discount_percentage
FROM tata_sales
GROUP BY discount_reason
ORDER BY discount_percentage DESC; 

-- Query 3 First-time buyer % by region

SELECT region,
       ROUND(SUM(CASE WHEN is_first_time_buyer = 'True' THEN 1 ELSE 'False' END) * 100.0 / COUNT(*), 2) AS first_time_buyer_pct
FROM tata_sales
GROUP BY region
ORDER BY first_time_buyer_pct DESC;    

use tata_motors;

-- Query 4  Sales Channel Performance
 
SELECT sales_channel,
       SUM(units_sold) AS total_sold,
       ROUND(AVG(dealer_discount_pct), 2) AS discount_percentage,
       ROUND(AVG(customer_rating), 2) AS customer_ratings 
FROM tata_sales      
GROUP BY sales_channel
ORDER BY total_sold DESC; 

use tata_motors;

-- Query 5  Year over Year Growth Rate

WITH yearly AS (
    SELECT year,
           SUM(units_sold * average_sale_price) AS total_revenue
    FROM tata_sales
    GROUP BY year
)
SELECT year,
       total_revenue,
       LAG(total_revenue) OVER (ORDER BY year) AS prev_year_revenue,
       ROUND((total_revenue - LAG(total_revenue) OVER (ORDER BY year)) 
       / LAG(total_revenue) OVER (ORDER BY year) * 100, 2) AS yoy_growth
FROM yearly
ORDER BY year;
 
          
      
      
 
    


