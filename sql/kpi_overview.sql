-- Key Performance Indicators (KPIs) Query
-- Total Revenue
SELECT 
    SUM(sales_amount) as total_revenue,
    COUNT(*) as total_transactions,
    COUNT(DISTINCT customer_id) as total_customers,
    SUM(units_sold) as total_units_sold,
    AVG(sales_amount) as avg_transaction_value
FROM enriched_sales;