import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import os
import yaml
from datetime import datetime

class EmailNotifier:
    def __init__(self, config_path="config.yaml"):
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                self.email_config = config['email']
        except Exception as e:
            print(f"⚠️ Config error: {e}")
            # Set Mailtrap defaults for testing
            self.email_config = {
                'enabled': True,
                'smtp_server': "sandbox.smtp.mailtrap.io",
                'smtp_port': 2525,
                'sender_email': "test@data-automation.com",
                'sender_password': "ca42c456469cd2",  # Your Mailtrap password
                'recipients': ["team@company.com"]
            }
            
    def send_email(self, subject, body, attachments=[]):
        """Send email with optional attachments"""
        if not self.email_config['enabled']:
            print("📧 Email notifications disabled in config")
            return False
            
        try:
            # Create message
            msg = MimeMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ", ".join(self.email_config['recipients'])
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MimeText(body, 'plain'))
            
            # Add attachments
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    with open(attachment_path, 'rb') as file:
                        part = MimeBase('application', 'octet-stream')
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(attachment_path)}'
                    )
                    msg.attach(part)
            
            # Send email using your Mailtrap credentials
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login("5e87660b6bef5c", self.email_config['sender_password'])
                text = msg.as_string()
                server.sendmail(self.email_config['sender_email'], self.email_config['recipients'], text)
            
            print(f"✅ Email sent successfully to {len(self.email_config['recipients'])} recipients")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
            
    def send_analysis_report(self, analysis_report, attachments=[]):
        """Specialized method for sending analysis reports"""
        subject = f"📊 Automated Sales Analysis Report - {datetime.now().strftime('%Y-%m-%d')}"
        
        body = f"""
Good morning team,

Here is your automated sales analysis report generated at {datetime.now().strftime('%H:%M:%S')}.

{analysis_report}

Best regards,
Data Automation System
"""
        
        return self.send_email(subject, body, attachments)
