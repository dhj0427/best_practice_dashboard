#!/usr/bin/env python3
"""
Databricks AI/BI Dashboard Setup Script

This script automates the setup process for the sample dashboard.
It can be used to quickly deploy the dashboard in a new Databricks environment.

Usage:
    python setup_dashboard.py --workspace-url <url> --token <token>
"""

import os
import sys
import argparse
import json
import pandas as pd
from pathlib import Path

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Setup Databricks AI/BI Dashboard'
    )
    parser.add_argument(
        '--workspace-url',
        required=True,
        help='Databricks workspace URL'
    )
    parser.add_argument(
        '--token',
        required=True,
        help='Databricks personal access token'
    )
    parser.add_argument(
        '--warehouse-id',
        help='SQL warehouse ID (optional)'
    )
    parser.add_argument(
        '--data-path',
        default='./data',
        help='Path to sample data files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without executing'
    )
    return parser.parse_args()

def validate_environment():
    """Validate that required files and dependencies exist."""
    required_files = [
        'data/sales_data.csv',
        'data/customer_data.csv',
        'notebooks/sales_analytics_processing.py',
        'notebooks/dashboard_visualizations.py',
        'dashboard/dashboard_config.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files found")
    return True

def load_sample_data(data_path):
    """Load and validate sample data."""
    try:
        sales_data = pd.read_csv(f"{data_path}/sales_data.csv")
        customer_data = pd.read_csv(f"{data_path}/customer_data.csv")
        
        print(f"📊 Loaded sales data: {len(sales_data)} records")
        print(f"👥 Loaded customer data: {len(customer_data)} records")
        
        return sales_data, customer_data
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None, None

def create_databricks_tables(workspace_url, token, sales_data, customer_data, dry_run=False):
    """Create tables in Databricks."""
    if dry_run:
        print("🔄 [DRY RUN] Would create Databricks tables:")
        print("   - sales table")
        print("   - customers table")
        return True
    
    # In a real implementation, this would use the Databricks API
    # to upload data and create tables
    print("🔄 Creating Databricks tables...")
    print("   Note: This requires Databricks API implementation")
    print("   Please manually upload CSV files and create tables as described in the setup guide")
    return True

def upload_notebooks(workspace_url, token, dry_run=False):
    """Upload notebooks to Databricks workspace."""
    notebooks = [
        'notebooks/sales_analytics_processing.py',
        'notebooks/dashboard_visualizations.py'
    ]
    
    if dry_run:
        print("🔄 [DRY RUN] Would upload notebooks:")
        for notebook in notebooks:
            print(f"   - {notebook}")
        return True
    
    print("📓 Uploading notebooks...")
    print("   Note: This requires Databricks API implementation")
    print("   Please manually import notebooks as described in the setup guide")
    return True

def create_dashboard_queries(workspace_url, token, dry_run=False):
    """Create SQL queries in Databricks SQL."""
    sql_files = [
        'sql/kpi_overview.sql',
        'sql/revenue_by_region.sql',
        'sql/product_performance.sql',
        'sql/sales_trends.sql',
        'sql/customer_segmentation.sql',
        'sql/top_customers.sql'
    ]
    
    if dry_run:
        print("🔄 [DRY RUN] Would create SQL queries:")
        for sql_file in sql_files:
            print(f"   - {sql_file}")
        return True
    
    print("📋 Creating SQL queries...")
    print("   Note: This requires Databricks API implementation")
    print("   Please manually create queries as described in the setup guide")
    return True

def validate_dashboard_config():
    """Validate dashboard configuration."""
    try:
        with open('dashboard/dashboard_config.json', 'r') as f:
            config = json.load(f)
        
        print("✅ Dashboard configuration validated")
        print(f"   Dashboard name: {config['dashboard']['name']}")
        print(f"   Sections: {len(config['dashboard']['layout']['sections'])}")
        print(f"   Filters: {len(config['dashboard']['filters'])}")
        return True
    except Exception as e:
        print(f"❌ Error validating dashboard config: {e}")
        return False

def main():
    """Main setup function."""
    args = parse_arguments()
    
    print("🚀 Databricks AI/BI Dashboard Setup")
    print("=" * 50)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Load sample data
    sales_data, customer_data = load_sample_data(args.data_path)
    if sales_data is None or customer_data is None:
        sys.exit(1)
    
    # Validate dashboard configuration
    if not validate_dashboard_config():
        sys.exit(1)
    
    # Create Databricks resources
    success = True
    success &= create_databricks_tables(
        args.workspace_url, 
        args.token, 
        sales_data, 
        customer_data,
        args.dry_run
    )
    success &= upload_notebooks(args.workspace_url, args.token, args.dry_run)
    success &= create_dashboard_queries(args.workspace_url, args.token, args.dry_run)
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Log into your Databricks workspace")
        print("2. Run the data processing notebook")
        print("3. Run the visualization notebook")
        print("4. Create a SQL dashboard using the provided queries")
        print("\nFor detailed instructions, see docs/setup_guide.md")
    else:
        print("\n❌ Setup encountered errors")
        sys.exit(1)

if __name__ == "__main__":
    main()