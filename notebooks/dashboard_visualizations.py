# Databricks notebook source
# MAGIC %md
# MAGIC # Sales Analytics Dashboard - Visualizations
# MAGIC 
# MAGIC This notebook creates the visualizations for the Databricks AI/BI Dashboard.
# MAGIC This notebook should be run after the data processing notebook.

# COMMAND ----------

# Import required libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Set style
sns.set_style("whitegrid")
plt.style.use('default')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Key Performance Indicators Dashboard

# COMMAND ----------

# MAGIC %sql
# MAGIC -- KPI Overview
# MAGIC SELECT 
# MAGIC     SUM(sales_amount) as total_revenue,
# MAGIC     COUNT(*) as total_transactions,
# MAGIC     COUNT(DISTINCT customer_id) as total_customers,
# MAGIC     AVG(sales_amount) as avg_transaction_value,
# MAGIC     SUM(units_sold) as total_units_sold
# MAGIC FROM enriched_sales

# COMMAND ----------

# MAGIC %md
# MAGIC ## Revenue Analysis by Region

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     region,
# MAGIC     SUM(sales_amount) as revenue,
# MAGIC     COUNT(*) as transactions,
# MAGIC     COUNT(DISTINCT customer_id) as customers,
# MAGIC     AVG(sales_amount) as avg_order_value
# MAGIC FROM enriched_sales
# MAGIC GROUP BY region
# MAGIC ORDER BY revenue DESC

# COMMAND ----------

# Create interactive regional analysis
regional_data = spark.sql("""
    SELECT 
        region,
        SUM(sales_amount) as revenue,
        COUNT(*) as transactions,
        COUNT(DISTINCT customer_id) as customers,
        AVG(sales_amount) as avg_order_value
    FROM enriched_sales
    GROUP BY region
    ORDER BY revenue DESC
""").toPandas()

# Create bar chart
fig = px.bar(regional_data, 
             x='region', 
             y='revenue',
             title='Revenue by Region',
             color='region',
             text='revenue')

fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
fig.update_layout(showlegend=False, yaxis_title='Revenue ($)')
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Product Category Performance

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     product_category,
# MAGIC     SUM(sales_amount) as revenue,
# MAGIC     COUNT(*) as transactions,
# MAGIC     COUNT(DISTINCT customer_id) as customers,
# MAGIC     ROUND(SUM(sales_amount) / (SELECT SUM(sales_amount) FROM enriched_sales) * 100, 2) as revenue_share
# MAGIC FROM enriched_sales
# MAGIC GROUP BY product_category
# MAGIC ORDER BY revenue DESC

# COMMAND ----------

# Product performance visualization
product_data = spark.sql("""
    SELECT 
        product_category,
        SUM(sales_amount) as revenue,
        COUNT(*) as transactions,
        ROUND(SUM(sales_amount) / (SELECT SUM(sales_amount) FROM enriched_sales) * 100, 2) as revenue_share
    FROM enriched_sales
    GROUP BY product_category
    ORDER BY revenue DESC
""").toPandas()

# Create subplot with bar chart and pie chart
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Product Revenue', 'Market Share'),
    specs=[[{"type": "xy"}, {"type": "domain"}]]
)

# Bar chart
fig.add_trace(
    go.Bar(x=product_data['product_category'], 
           y=product_data['revenue'],
           name='Revenue',
           marker_color='steelblue'),
    row=1, col=1
)

# Pie chart
fig.add_trace(
    go.Pie(labels=product_data['product_category'], 
           values=product_data['revenue_share'],
           name="Market Share"),
    row=1, col=2
)

fig.update_layout(title_text="Product Category Analysis")
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sales Trends Over Time

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     date,
# MAGIC     SUM(sales_amount) as daily_revenue,
# MAGIC     COUNT(*) as daily_transactions,
# MAGIC     AVG(sales_amount) as avg_daily_order_value,
# MAGIC     AVG(SUM(sales_amount)) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_3day_avg
# MAGIC FROM enriched_sales
# MAGIC GROUP BY date
# MAGIC ORDER BY date

# COMMAND ----------

# Time series analysis
trend_data = spark.sql("""
    SELECT 
        date,
        SUM(sales_amount) as daily_revenue,
        COUNT(*) as daily_transactions,
        AVG(SUM(sales_amount)) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_3day_avg
    FROM enriched_sales
    GROUP BY date
    ORDER BY date
""").toPandas()

# Create time series plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=trend_data['date'],
    y=trend_data['daily_revenue'],
    mode='lines+markers',
    name='Daily Revenue',
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=trend_data['date'],
    y=trend_data['rolling_3day_avg'],
    mode='lines',
    name='3-Day Rolling Average',
    line=dict(color='red', dash='dash')
))

fig.update_layout(
    title='Daily Sales Revenue Trend',
    xaxis_title='Date',
    yaxis_title='Revenue ($)',
    hovermode='x unified'
)

fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Customer Segmentation Analysis

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     subscription_tier,
# MAGIC     age_group,
# MAGIC     COUNT(DISTINCT customer_id) as customer_count,
# MAGIC     SUM(sales_amount) as total_revenue,
# MAGIC     AVG(sales_amount) as avg_revenue_per_transaction,
# MAGIC     COUNT(*) as total_transactions
# MAGIC FROM enriched_sales
# MAGIC GROUP BY subscription_tier, age_group
# MAGIC ORDER BY subscription_tier, total_revenue DESC

# COMMAND ----------

# Customer segmentation heatmap
segmentation_data = spark.sql("""
    SELECT 
        subscription_tier,
        age_group,
        COUNT(DISTINCT customer_id) as customer_count,
        SUM(sales_amount) as total_revenue
    FROM enriched_sales
    GROUP BY subscription_tier, age_group
""").toPandas()

# Pivot for heatmap
heatmap_data = segmentation_data.pivot(index='subscription_tier', 
                                      columns='age_group', 
                                      values='total_revenue').fillna(0)

# Create heatmap
fig = px.imshow(heatmap_data, 
                text_auto=True, 
                aspect="auto",
                title="Customer Segmentation: Revenue by Tier and Age Group")

fig.update_traces(texttemplate="$%{text:,.0f}")
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Top Performing Customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     customer_name,
# MAGIC     subscription_tier,
# MAGIC     region,
# MAGIC     COUNT(*) as total_transactions,
# MAGIC     SUM(sales_amount) as lifetime_value,
# MAGIC     AVG(sales_amount) as avg_order_value,
# MAGIC     MAX(date) as last_purchase_date
# MAGIC FROM enriched_sales
# MAGIC GROUP BY customer_id, customer_name, subscription_tier, region
# MAGIC ORDER BY lifetime_value DESC
# MAGIC LIMIT 15

# COMMAND ----------

# Top customers analysis
top_customers = spark.sql("""
    SELECT 
        customer_name,
        subscription_tier,
        region,
        COUNT(*) as total_transactions,
        SUM(sales_amount) as lifetime_value,
        AVG(sales_amount) as avg_order_value
    FROM enriched_sales
    GROUP BY customer_id, customer_name, subscription_tier, region
    ORDER BY lifetime_value DESC
    LIMIT 10
""").toPandas()

# Create horizontal bar chart
fig = px.bar(top_customers,
             x='lifetime_value',
             y='customer_name',
             color='subscription_tier',
             title='Top 10 Customers by Lifetime Value',
             orientation='h')

fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Advanced Analytics - Cohort Analysis Preview

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Customer acquisition by signup month
# MAGIC SELECT 
# MAGIC     DATE_TRUNC('month', c.signup_date) as signup_month,
# MAGIC     COUNT(DISTINCT c.customer_id) as new_customers,
# MAGIC     SUM(s.sales_amount) as total_revenue_generated,
# MAGIC     AVG(s.sales_amount) as avg_revenue_per_new_customer
# MAGIC FROM customers c
# MAGIC JOIN enriched_sales s ON c.customer_id = s.customer_id
# MAGIC GROUP BY DATE_TRUNC('month', c.signup_date)
# MAGIC ORDER BY signup_month

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary Dashboard Metrics

# COMMAND ----------

# Create comprehensive summary
summary_metrics = spark.sql("""
    SELECT 
        'Total Revenue' as metric,
        CONCAT('$', FORMAT_NUMBER(SUM(sales_amount), 0)) as value
    FROM enriched_sales
    
    UNION ALL
    
    SELECT 
        'Total Customers' as metric,
        FORMAT_NUMBER(COUNT(DISTINCT customer_id), 0) as value
    FROM enriched_sales
    
    UNION ALL
    
    SELECT 
        'Average Order Value' as metric,
        CONCAT('$', FORMAT_NUMBER(AVG(sales_amount), 2)) as value
    FROM enriched_sales
    
    UNION ALL
    
    SELECT 
        'Best Performing Region' as metric,
        region as value
    FROM (
        SELECT region, SUM(sales_amount) as revenue
        FROM enriched_sales
        GROUP BY region
        ORDER BY revenue DESC
        LIMIT 1
    )
    
    UNION ALL
    
    SELECT 
        'Top Product Category' as metric,
        product_category as value
    FROM (
        SELECT product_category, SUM(sales_amount) as revenue
        FROM enriched_sales
        GROUP BY product_category
        ORDER BY revenue DESC
        LIMIT 1
    )
""")

display(summary_metrics)

# COMMAND ----------

print("Dashboard visualization notebook completed successfully!")
print("All charts and visualizations are ready for the Databricks AI/BI Dashboard.")