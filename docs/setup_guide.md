# Databricks AI/BI Dashboard Setup Guide

## Overview
This repository contains a comprehensive sample Databricks AI/BI dashboard that demonstrates best practices for sales analytics and customer intelligence. The dashboard includes data processing pipelines, interactive visualizations, and key business metrics.

## Architecture

```
best_practice_dashboard/
├── data/                           # Sample datasets
│   ├── sales_data.csv             # Transaction data
│   └── customer_data.csv          # Customer demographics
├── notebooks/                      # Databricks notebooks
│   ├── sales_analytics_processing.py    # Data processing pipeline
│   └── dashboard_visualizations.py      # Visualization notebook
├── sql/                           # SQL queries for dashboard
│   ├── kpi_overview.sql           # Key performance indicators
│   ├── revenue_by_region.sql      # Regional analysis
│   ├── product_performance.sql    # Product analytics
│   ├── sales_trends.sql           # Time series analysis
│   ├── customer_segmentation.sql  # Customer analysis
│   └── top_customers.sql          # Customer rankings
├── dashboard/                     # Dashboard configuration
│   └── dashboard_config.json      # Layout and widget definitions
└── docs/                          # Documentation
    └── setup_guide.md             # This file
```

## Quick Start

### Prerequisites
- Databricks workspace with Unity Catalog enabled
- SQL Warehouse or compute cluster running
- Access to file upload capabilities in Databricks

### Step 1: Upload Sample Data

1. Navigate to your Databricks workspace
2. Go to **Data** > **Create Table**
3. Upload the following CSV files from the `data/` directory:
   - `sales_data.csv`
   - `customer_data.csv`
4. Create tables named `sales` and `customers` respectively

Alternatively, upload files to DBFS:
```sql
-- Upload files to /FileStore/shared_uploads/ in Databricks
-- Then create tables:
CREATE TABLE sales USING CSV
OPTIONS (path '/FileStore/shared_uploads/sales_data.csv', header 'true', inferSchema 'true');

CREATE TABLE customers USING CSV
OPTIONS (path '/FileStore/shared_uploads/customer_data.csv', header 'true', inferSchema 'true');
```

### Step 2: Run Data Processing Notebook

1. Import `notebooks/sales_analytics_processing.py` into your Databricks workspace
2. Attach it to a cluster or SQL warehouse
3. Run all cells to:
   - Load and validate the data
   - Create enriched views
   - Generate processed tables for dashboard consumption
   - Export summary datasets

### Step 3: Create Dashboard Visualizations

1. Import `notebooks/dashboard_visualizations.py` into your workspace
2. Run the notebook to generate interactive charts and visualizations
3. The notebook creates various chart types:
   - KPI metrics
   - Revenue by region (bar chart and pie chart)
   - Product performance analysis
   - Time series trends
   - Customer segmentation heatmap
   - Top customer rankings

### Step 4: Set Up Databricks SQL Dashboard

1. Navigate to **SQL** > **Dashboards** in your Databricks workspace
2. Click **Create Dashboard**
3. Use the SQL queries from the `sql/` directory to create visualizations:

#### Create Queries:
- Import each `.sql` file as a new query in Databricks SQL
- Name them according to their function (e.g., "KPI Overview", "Revenue by Region")

#### Add Visualizations:
- For each query, create appropriate visualizations:
  - **KPI Overview**: Counter/Number widgets
  - **Revenue by Region**: Bar chart and pie chart
  - **Product Performance**: Horizontal bar chart
  - **Sales Trends**: Line chart
  - **Customer Segmentation**: Table or pivot visualization
  - **Top Customers**: Table with conditional formatting

#### Dashboard Layout:
Use the `dashboard/dashboard_config.json` as a reference for:
- Widget sizing and positioning
- Color schemes and formatting
- Filter configurations
- Refresh settings

## Key Features

### Data Sources
- **Sales Data**: Transaction-level data with dates, regions, products, and amounts
- **Customer Data**: Demographics including age, location, subscription tiers

### Key Metrics Tracked
- **Revenue KPIs**: Total revenue, average order value, transaction count
- **Geographic Analysis**: Performance by region with market share
- **Product Analytics**: Category performance and revenue contribution
- **Customer Intelligence**: Segmentation, lifetime value, top performers
- **Trend Analysis**: Daily sales patterns with moving averages

### Interactive Features
- **Date Range Filters**: Analyze performance over specific time periods
- **Geographic Filters**: Focus on specific regions
- **Product Filters**: Filter by product categories
- **Customer Segment Filters**: Analyze specific customer groups

## Advanced Usage

### Custom Metrics
To add custom metrics, modify the SQL queries and add new visualizations:

1. Create new SQL queries in the `sql/` directory
2. Add corresponding sections to `dashboard_config.json`
3. Update the visualization notebook if needed

### Automated Refresh
Configure automatic refresh in Databricks SQL Dashboard:
1. Set up scheduled refresh for underlying data tables
2. Configure dashboard auto-refresh intervals
3. Set up alerts for significant metric changes

### Integration with External Tools
The processed data can be exported for use in other BI tools:
- Export processed tables as CSV/Parquet
- Use Databricks Connect for programmatic access
- Set up data sharing through Delta Sharing

## Best Practices Demonstrated

### Data Quality
- Data validation and quality checks
- Handling missing values and duplicates
- Schema enforcement and data types

### Performance Optimization
- Efficient data processing with Spark SQL
- Proper table partitioning strategies
- Query optimization techniques
- Caching strategies for dashboard performance

### Security and Governance
- Unity Catalog integration
- Row-level security examples
- Audit trail and lineage tracking
- Data access controls

### Visualization Design
- Clean, professional dashboard layouts
- Color-coded metrics and KPIs
- Interactive filtering capabilities
- Mobile-responsive design considerations

## Troubleshooting

### Common Issues
1. **Data Upload Errors**: Ensure CSV files have proper headers and encoding
2. **Query Failures**: Check table names match your environment
3. **Visualization Issues**: Verify data types are correct for chart types
4. **Performance Problems**: Consider data volume and cluster size

### Getting Help
- Check Databricks documentation for specific errors
- Review Unity Catalog permissions
- Validate SQL syntax in Databricks SQL editor
- Test queries incrementally

## Next Steps
- Scale with larger datasets
- Add more sophisticated ML models
- Implement real-time streaming analytics
- Create automated reporting workflows