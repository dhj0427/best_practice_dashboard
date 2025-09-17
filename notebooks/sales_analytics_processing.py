# Databricks notebook source
# MAGIC %md
# MAGIC # Sales Analytics Dashboard - Data Processing
# MAGIC 
# MAGIC This notebook processes sales and customer data to create insights for the AI/BI dashboard.
# MAGIC 
# MAGIC ## Data Sources:
# MAGIC - Sales transaction data
# MAGIC - Customer demographic data
# MAGIC 
# MAGIC ## Key Metrics:
# MAGIC - Total revenue by region and product category
# MAGIC - Customer segmentation analysis
# MAGIC - Sales trends over time
# MAGIC - Customer lifetime value

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Data Import and Setup

# COMMAND ----------

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Set display options
pd.set_option('display.max_columns', None)
spark.conf.set("spark.sql.adaptive.enabled", "true")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Load Data

# COMMAND ----------

# Load sales data
sales_df = spark.read.option("header", "true").option("inferSchema", "true").csv("/FileStore/shared_uploads/sales_data.csv")
sales_df.createOrReplaceTempView("sales")

# Load customer data  
customer_df = spark.read.option("header", "true").option("inferSchema", "true").csv("/FileStore/shared_uploads/customer_data.csv")
customer_df.createOrReplaceTempView("customers")

# Display basic info
print("Sales Data Schema:")
sales_df.printSchema()
print(f"Sales Records: {sales_df.count()}")

print("\nCustomer Data Schema:")
customer_df.printSchema()
print(f"Customer Records: {customer_df.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Data Quality and Exploration

# COMMAND ----------

# Check for missing values and data quality
print("Sales Data Summary:")
display(sales_df.describe())

print("\nCustomer Data Summary:")
display(customer_df.describe())

# Check for duplicates
print(f"Duplicate sales records: {sales_df.count() - sales_df.distinct().count()}")
print(f"Duplicate customer records: {customer_df.count() - customer_df.distinct().count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Create Enriched Dataset

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create enriched sales view with customer information
# MAGIC CREATE OR REPLACE VIEW enriched_sales AS
# MAGIC SELECT 
# MAGIC     s.date,
# MAGIC     s.region,
# MAGIC     s.product_category,
# MAGIC     s.sales_amount,
# MAGIC     s.units_sold,
# MAGIC     s.customer_id,
# MAGIC     c.customer_name,
# MAGIC     c.age,
# MAGIC     c.gender,
# MAGIC     c.location,
# MAGIC     c.signup_date,
# MAGIC     c.subscription_tier,
# MAGIC     DATEDIFF(s.date, c.signup_date) as days_since_signup,
# MAGIC     CASE 
# MAGIC         WHEN c.age < 30 THEN 'Young (18-29)'
# MAGIC         WHEN c.age < 40 THEN 'Middle (30-39)'
# MAGIC         ELSE 'Mature (40+)'
# MAGIC     END as age_group
# MAGIC FROM sales s
# MAGIC JOIN customers c ON s.customer_id = c.customer_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Key Business Metrics

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Total Revenue by Region
# MAGIC SELECT 
# MAGIC     region,
# MAGIC     COUNT(*) as transaction_count,
# MAGIC     SUM(sales_amount) as total_revenue,
# MAGIC     AVG(sales_amount) as avg_transaction_value,
# MAGIC     SUM(units_sold) as total_units
# MAGIC FROM enriched_sales
# MAGIC GROUP BY region
# MAGIC ORDER BY total_revenue DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Product Category Performance
# MAGIC SELECT 
# MAGIC     product_category,
# MAGIC     COUNT(*) as transaction_count,
# MAGIC     SUM(sales_amount) as total_revenue,
# MAGIC     AVG(sales_amount) as avg_transaction_value,
# MAGIC     SUM(units_sold) as total_units,
# MAGIC     ROUND(SUM(sales_amount) / SUM(SUM(sales_amount)) OVER() * 100, 2) as revenue_percentage
# MAGIC FROM enriched_sales
# MAGIC GROUP BY product_category
# MAGIC ORDER BY total_revenue DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Customer Segmentation Analysis

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Customer Segmentation by Subscription Tier
# MAGIC SELECT 
# MAGIC     subscription_tier,
# MAGIC     age_group,
# MAGIC     COUNT(DISTINCT customer_id) as customer_count,
# MAGIC     SUM(sales_amount) as total_revenue,
# MAGIC     AVG(sales_amount) as avg_revenue_per_customer,
# MAGIC     ROUND(AVG(units_sold), 2) as avg_units_per_transaction
# MAGIC FROM enriched_sales
# MAGIC GROUP BY subscription_tier, age_group
# MAGIC ORDER BY subscription_tier, age_group

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Time-based Analysis

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Daily Sales Trend
# MAGIC SELECT 
# MAGIC     date,
# MAGIC     COUNT(*) as daily_transactions,
# MAGIC     SUM(sales_amount) as daily_revenue,
# MAGIC     AVG(sales_amount) as avg_transaction_value,
# MAGIC     SUM(units_sold) as daily_units
# MAGIC FROM enriched_sales
# MAGIC GROUP BY date
# MAGIC ORDER BY date

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Advanced Analytics - Customer Lifetime Value

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Customer Lifetime Value Analysis
# MAGIC CREATE OR REPLACE VIEW customer_clv AS
# MAGIC SELECT 
# MAGIC     customer_id,
# MAGIC     customer_name,
# MAGIC     subscription_tier,
# MAGIC     age_group,
# MAGIC     region,
# MAGIC     COUNT(*) as total_transactions,
# MAGIC     SUM(sales_amount) as total_spent,
# MAGIC     AVG(sales_amount) as avg_order_value,
# MAGIC     MAX(date) as last_purchase_date,
# MAGIC     MIN(date) as first_purchase_date,
# MAGIC     DATEDIFF(MAX(date), MIN(date)) as customer_lifespan_days,
# MAGIC     SUM(units_sold) as total_units_purchased
# MAGIC FROM enriched_sales
# MAGIC GROUP BY customer_id, customer_name, subscription_tier, age_group, region

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Top Customers by Value
# MAGIC SELECT 
# MAGIC     customer_name,
# MAGIC     subscription_tier,
# MAGIC     region,
# MAGIC     total_spent,
# MAGIC     total_transactions,
# MAGIC     avg_order_value,
# MAGIC     customer_lifespan_days
# MAGIC FROM customer_clv
# MAGIC ORDER BY total_spent DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Create Tables for Dashboard

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create final tables for dashboard consumption
# MAGIC 
# MAGIC -- Regional Performance Summary
# MAGIC CREATE OR REPLACE TABLE dashboard_regional_performance AS
# MAGIC SELECT 
# MAGIC     region,
# MAGIC     COUNT(*) as transaction_count,
# MAGIC     SUM(sales_amount) as total_revenue,
# MAGIC     AVG(sales_amount) as avg_transaction_value,
# MAGIC     COUNT(DISTINCT customer_id) as unique_customers,
# MAGIC     SUM(units_sold) as total_units_sold
# MAGIC FROM enriched_sales
# MAGIC GROUP BY region;
# MAGIC 
# MAGIC -- Product Performance Summary
# MAGIC CREATE OR REPLACE TABLE dashboard_product_performance AS
# MAGIC SELECT 
# MAGIC     product_category,
# MAGIC     COUNT(*) as transaction_count,
# MAGIC     SUM(sales_amount) as total_revenue,
# MAGIC     AVG(sales_amount) as avg_transaction_value,
# MAGIC     COUNT(DISTINCT customer_id) as unique_customers,
# MAGIC     SUM(units_sold) as total_units_sold,
# MAGIC     ROUND(SUM(sales_amount) / (SELECT SUM(sales_amount) FROM enriched_sales) * 100, 2) as revenue_share_percent
# MAGIC FROM enriched_sales
# MAGIC GROUP BY product_category;
# MAGIC 
# MAGIC -- Daily Trends
# MAGIC CREATE OR REPLACE TABLE dashboard_daily_trends AS
# MAGIC SELECT 
# MAGIC     date,
# MAGIC     COUNT(*) as transaction_count,
# MAGIC     SUM(sales_amount) as daily_revenue,
# MAGIC     AVG(sales_amount) as avg_transaction_value,
# MAGIC     COUNT(DISTINCT customer_id) as daily_unique_customers,
# MAGIC     SUM(units_sold) as daily_units_sold
# MAGIC FROM enriched_sales
# MAGIC GROUP BY date
# MAGIC ORDER BY date;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Data Export for External Tools

# COMMAND ----------

# Export key datasets for external dashboard tools if needed
regional_performance = spark.sql("SELECT * FROM dashboard_regional_performance").toPandas()
product_performance = spark.sql("SELECT * FROM dashboard_product_performance").toPandas()
daily_trends = spark.sql("SELECT * FROM dashboard_daily_trends").toPandas()

# Save as CSV for external consumption
regional_performance.to_csv("/dbfs/FileStore/shared_uploads/dashboard_regional_performance.csv", index=False)
product_performance.to_csv("/dbfs/FileStore/shared_uploads/dashboard_product_performance.csv", index=False)
daily_trends.to_csv("/dbfs/FileStore/shared_uploads/dashboard_daily_trends.csv", index=False)

print("Data processing completed successfully!")
print(f"Regional Performance records: {len(regional_performance)}")
print(f"Product Performance records: {len(product_performance)}")
print(f"Daily Trends records: {len(daily_trends)}")