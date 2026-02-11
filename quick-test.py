import os
import yaml
from scripts.analyzer import DataAnalyzer
from scripts.email_notifier import EmailNotifier

def quick_test():
    """Test the complete system"""
    print("🧪 Running quick system test...")
    
    # Ensure directories exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Test data analyzer
    print("1. Testing data analyzer...")
    analyzer = DataAnalyzer()
    
    # Create minimal test data
    import pandas as pd
    test_data = pd.DataFrame({
        'InvoiceNo': ['INV001', 'INV002'],
        'StockCode': ['SKU001', 'SKU002'],
        'Description': ['Test Product A', 'Test Product B'],
        'Quantity': [2, 3],
        'InvoiceDate': ['2024-01-01 10:00:00', '2024-01-02 11:00:00'],
        'UnitPrice': [25.00, 15.00],
        'CustomerID': [12345, 67890],
        'Country': ['United Kingdom', 'Germany']
    })
    test_data.to_csv('data/raw/sample_sales_data.csv', index=False)
    
    # Analyze data
    df = analyzer.load_dataset()
    if df is not None:
        df_clean = analyzer.basic_cleaning(df)
        results = analyzer.sales_analysis(df_clean)
        report = analyzer.generate_report(results)
        
        print("✅ Data analysis successful!")
        
        # Test email
        print("2. Testing email notification...")
        notifier = EmailNotifier()
        
        # Create simple test files
        with open('reports/test_report.txt', 'w') as f:
            f.write("This is a test report file.")
        
        # Send test email
        success = notifier.send_email(
            subject="🧪 System Test Complete",
            body=f"Data Automation System Test Successful!\n\n{report}",
            attachments=['reports/test_report.txt']
        )
        
        if success:
            print("🎉 System test completed successfully!")
            print("📨 Check Mailtrap for the test email")
        else:
            print("⚠️ Email test failed, but system is functional")
    
    else:
        print("❌ Data loading failed")

if __name__ == "__main__":
    quick_test()
