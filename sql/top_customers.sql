-- Top Performing Customers
SELECT 
    customer_id,
    customer_name,
    subscription_tier,
    age_group,
    region,
    location,
    COUNT(*) as total_transactions,
    SUM(sales_amount) as lifetime_value,
    AVG(sales_amount) as avg_order_value,
    SUM(units_sold) as total_units_purchased,
    MAX(date) as last_purchase_date,
    MIN(date) as first_purchase_date,
    DATEDIFF(MAX(date), MIN(date)) + 1 as customer_lifespan_days,
    ROUND(SUM(sales_amount) / (DATEDIFF(MAX(date), MIN(date)) + 1), 2) as daily_avg_spend
FROM enriched_sales
GROUP BY customer_id, customer_name, subscription_tier, age_group, region, location
ORDER BY lifetime_value DESC
LIMIT 20;