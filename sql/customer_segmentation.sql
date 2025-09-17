-- Customer Segmentation Analysis
SELECT 
    subscription_tier,
    age_group,
    gender,
    COUNT(DISTINCT customer_id) as customer_count,
    SUM(sales_amount) as total_revenue,
    AVG(sales_amount) as avg_revenue_per_customer,
    COUNT(*) as total_transactions,
    ROUND(AVG(sales_amount), 2) as avg_transaction_value,
    SUM(units_sold) as total_units,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT customer_id), 2) as avg_transactions_per_customer
FROM enriched_sales
GROUP BY subscription_tier, age_group, gender
ORDER BY subscription_tier, total_revenue DESC;