-- Revenue by Region Analysis
SELECT 
    region,
    SUM(sales_amount) as revenue,
    COUNT(*) as transactions,
    COUNT(DISTINCT customer_id) as customers,
    AVG(sales_amount) as avg_order_value,
    SUM(units_sold) as units_sold,
    ROUND(SUM(sales_amount) / (SELECT SUM(sales_amount) FROM enriched_sales) * 100, 2) as revenue_percentage
FROM enriched_sales
GROUP BY region
ORDER BY revenue DESC;