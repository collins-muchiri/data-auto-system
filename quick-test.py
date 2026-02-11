import os
import pandas as pd
from scripts.analyzer import analyze_data, process_directory
from scripts.email_notifier import EmailNotifier

def quick_test():
    """Test the complete system"""
    print("[TEST] Running quick system test...")

    # Ensure directories exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

    # Create minimal test data
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

    # Test data analyzer
    print("1. Testing data analyzer...")
    insights = analyze_data('data/raw/sample_sales_data.csv')
    
    if insights:
        print("[SUCCESS] Data analysis successful!")
        print(f"   - Data shape: {insights['shape']}")
        print(f"   - Columns: {insights['columns']}")
        print(f"   - Missing values: {sum(insights['missing_values'].values())}")
    else:
        print("[ERROR] Data analysis failed")
        return

    # Test email
    print("2. Testing email notification...")
    
    # Create simple test report
    with open('reports/test_report.txt', 'w') as f:
        f.write("This is a test report file.\n\n")
        f.write(f"Data Analysis Results:\n")
        f.write(f"- Shape: {insights['shape']}\n")
        f.write(f"- Columns: {insights['columns']}\n")
        f.write(f"- Missing Values: {insights['missing_values']}\n")

    # Create email notifier instance
    # Using the configuration from config.yaml
    notifier = EmailNotifier()

    # Send test email
    success = notifier.send_email(
        subject="[TEST] System Test Complete",
        body="Data Automation System Test Successful!\n\n"
             "This is a test email to verify the email notification functionality.",
        attachments=['reports/test_report.txt']
    )

    if success:
        print("[SUCCESS] System test completed successfully!")
        print("[INFO] Check Mailtrap for the test email")
    else:
        print("[WARNING] Email test failed, but system is functional (this is expected if using test credentials)")

if __name__ == "__main__":
    quick_test()
