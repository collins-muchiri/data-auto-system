# synthetic_data.py
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from pathlib import Path

def create_sample_sales_data(output_path='data/raw/sample_sales_data.csv', seed=42):
    """Create a sample e-commerce dataset"""
    np.random.seed(seed)

    # Generate sample data
    n_rows = 1000
    products = ['Red T-Shirt', 'Blue Jeans', 'Black Jacket', 'White Sneakers',
                'Green Backpack', 'Yellow Cap', 'Purple Hoodie', 'Orange Shorts']
    countries = ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain']

    data = []
    start_date = datetime(2024, 1, 1)

    for i in range(n_rows):
        invoice_date = start_date + timedelta(days=np.random.randint(0, 365))
        quantity = np.random.randint(1, 5)
        unit_price = round(np.random.uniform(10, 100), 2)
        customer_id = np.random.randint(1000, 9999)

        row = {
            'InvoiceNo': f'INV{np.random.randint(100000, 999999)}',
            'StockCode': f'SKU{np.random.randint(1000, 9999)}',
            'Description': np.random.choice(products),
            'Quantity': quantity,
            'InvoiceDate': invoice_date.strftime('%Y-%m-%d %H:%M:%S'),
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Country': np.random.choice(countries)
        }
        data.append(row)

    try:
        df = pd.DataFrame(data)
        
        # Create directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"[SUCCESS] Created sample dataset with {len(df)} rows at {output_path}")
        return df
    except Exception as e:
        print(f"[ERROR] Error creating dataset: {e}")
        return None

def validate_data(df):
    """Validate the generated data"""
    issues = []
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        issues.append(f"Missing values detected: {missing_values[missing_values > 0].to_dict()}")
    
    # Validate data types
    expected_types = {
        'Quantity': 'int',
        'UnitPrice': 'float',
        'CustomerID': 'int'
    }
    
    for col, expected_type in expected_types.items():
        if col in df.columns:
            if expected_type == 'int' and not pd.api.types.is_integer_dtype(df[col]):
                issues.append(f"Column '{col}' is not integer type")
            elif expected_type == 'float' and not pd.api.types.is_float_dtype(df[col]):
                issues.append(f"Column '{col}' is not float type")
    
    if issues:
        print("[WARNING] Validation issues found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("[SUCCESS] Data validation passed")
    
    return len(issues) == 0

if __name__ == "__main__":
    df = create_sample_sales_data()
    if df is not None:
        validate_data(df)
        print("\n[INFO] Dataset Info:")
        print(df.head())
        print(f"\n[INFO] Dataset Shape: {df.shape}")
        print(f"[INFO] Date Range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
