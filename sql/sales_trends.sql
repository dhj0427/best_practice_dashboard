-- Sales Trends Over Time
SELECT 
    date,
    SUM(sales_amount) as daily_revenue,
    COUNT(*) as daily_transactions,
    COUNT(DISTINCT customer_id) as daily_customers,
    AVG(sales_amount) as avg_daily_order_value,
    SUM(units_sold) as daily_units_sold,
    -- Rolling 3-day average
    AVG(SUM(sales_amount)) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_3day_avg
FROM enriched_sales
GROUP BY date
ORDER BY date;