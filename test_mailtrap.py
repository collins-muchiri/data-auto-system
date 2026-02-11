"""
Test script for Mailtrap email configuration
This script tests the email notification functionality using Mailtrap
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
import os
from pathlib import Path


def load_config(config_path="config.yaml"):
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file: {e}")
        return None


def test_mailtrap_connection(smtp_server, smtp_port, username, password, sender_email):
    """Test connection to Mailtrap SMTP server"""
    try:
        # Create a simple test message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = "test@your_mailtrap_inbox.com"  # Replace with actual test recipient
        msg['Subject'] = "Test Email from Data Auto System"

        body = """
        This is a test email from the Data Auto System.
        
        If you're seeing this, the Mailtrap configuration is working correctly!
        
        System Details:
        - Timestamp: {}
        - Service: Data Auto System Email Notifier
        - Status: Connection Test Successful
        
        This email was sent via Mailtrap for testing purposes.
        """.format(str(__import__('datetime').datetime.now()))

        msg.attach(MIMEText(body, 'plain'))

        # Connect to Mailtrap SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable encryption
        server.login(username, password)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, "test@your_mailtrap_inbox.com", text)
        server.quit()

        print("[SUCCESS] Successfully connected to Mailtrap and sent test email!")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to connect to Mailtrap: {str(e)}")
        return False


def test_mailtrap_with_config():
    """Test Mailtrap using configuration from config.yaml"""
    config = load_config()
    
    if not config or 'email' not in config:
        print("❌ Configuration file missing or email settings not found")
        return False
    
    email_config = config['email']
    
    # Check if using Mailtrap
    if 'mailtrap' in email_config.get('smtp_server', '').lower():
        print(f"[EMAIL] Testing Mailtrap configuration...")
        print(f"   SMTP Server: {email_config['smtp_server']}")
        print(f"   SMTP Port: {email_config['smtp_port']}")
        print(f"   Sender Email: {email_config['sender_email']}")
        
        success = test_mailtrap_connection(
            email_config['smtp_server'],
            email_config['smtp_port'],
            email_config['sender_email'],
            email_config.get('sender_password', ''),
            email_config['sender_email']
        )
        
        if success:
            print("\n[SUCCESS] Mailtrap test successful!")
            print("Your Data Auto System is configured to use Mailtrap for email testing.")
            print("Emails will be captured in your Mailtrap inbox instead of being sent to real recipients.")
        else:
            print("\n[ERROR] Mailtrap test failed!")
            print("Please check your Mailtrap configuration in config.yaml")
        
        return success
    else:
        print("[ERROR] Current configuration is not set up for Mailtrap")
        print("To use Mailtrap, update your config.yaml with Mailtrap SMTP settings:")
        print("""
email:
  smtp_server: "smtp.mailtrap.io"
  smtp_port: 587  # or 2525
  sender_email: "your_mailtrap_username"
  sender_password: "your_mailtrap_password"
        """)
        return False


def setup_mailtrap_demo_config():
    """Create a demo configuration for Mailtrap"""
    demo_config = {
        'email': {
            'smtp_server': 'smtp.mailtrap.io',
            'smtp_port': 587,
            'sender_email': 'your_mailtrap_username',
            'sender_password': 'your_mailtrap_password'
        },
        'paths': {
            'logs_dir': './logs'
        }
    }
    
    # Create logs directory if it doesn't exist
    Path(demo_config['paths']['logs_dir']).mkdir(exist_ok=True)
    
    # Save demo config to a separate file
    with open('mailtrap_demo_config.yaml', 'w') as f:
        yaml.dump(demo_config, f, default_flow_style=False)
    
    print("[INFO] Demo Mailtrap configuration saved to 'mailtrap_demo_config.yaml'")
    print("[NOTE] Remember to replace the placeholder values with your actual Mailtrap credentials!")


if __name__ == "__main__":
    print("[TEST] Testing Mailtrap Email Configuration for Data Auto System\n")
    
    # Test current configuration
    success = test_mailtrap_with_config()
    
    if not success:
        print("\n[INFO] Creating a demo Mailtrap configuration for reference...")
        setup_mailtrap_demo_config()
        
        print("\n[INSTRUCTIONS] To configure Mailtrap:")
        print("   1. Sign up at https://mailtrap.io")
        print("   2. Get your SMTP credentials from the demo inbox")
        print("   3. Update config.yaml with your Mailtrap credentials")
        print("   4. Run this script again to test the connection")