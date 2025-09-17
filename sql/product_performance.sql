-- Product Category Performance
SELECT 
    product_category,
    SUM(sales_amount) as revenue,
    COUNT(*) as transactions,
    COUNT(DISTINCT customer_id) as customers,
    AVG(sales_amount) as avg_order_value,
    SUM(units_sold) as units_sold,
    ROUND(SUM(sales_amount) / (SELECT SUM(sales_amount) FROM enriched_sales) * 100, 2) as revenue_share,
    ROUND(AVG(sales_amount / units_sold), 2) as avg_price_per_unit
FROM enriched_sales
GROUP BY product_category
ORDER BY revenue DESC;