"""
Scheduler Module
Manages automated execution of data processing tasks
"""
import schedule
import time
import subprocess
import logging
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/scheduler.log'),
        logging.StreamHandler()
    ]
)


def run_analyzer():
    """Run the data analyzer script"""
    try:
        result = subprocess.run(['python', 'analyzer.py'], 
                              cwd='.', 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            logging.info("Analyzer completed successfully")
        else:
            logging.error(f"Analyzer failed: {result.stderr}")
    except Exception as e:
        logging.error(f"Error running analyzer: {str(e)}")


def run_email_notifier():
    """Run the email notifier script"""
    try:
        result = subprocess.run(['python', 'email_notifier.py'], 
                              cwd='.', 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            logging.info("Email notifier completed successfully")
        else:
            logging.error(f"Email notifier failed: {result.stderr}")
    except Exception as e:
        logging.error(f"Error running email notifier: {str(e)}")


def setup_schedules(config):
    """Set up scheduled tasks based on configuration"""
    # Schedule analyzer to run daily at 2 AM
    schedule.every().day.at("02:00").do(run_analyzer)
    
    # Schedule email notifications weekly on Mondays at 9 AM
    schedule.every().monday.at("09:00").do(run_email_notifier)
    
    # Add more schedules based on config if needed
    if 'custom_schedule' in config:
        for task, timing in config['custom_schedule'].items():
            if task == 'analyzer':
                if timing.get('frequency') == 'daily':
                    schedule.every().day.at(timing.get('time', '02:00')).do(run_analyzer)
            elif task == 'email_notifier':
                if timing.get('frequency') == 'weekly':
                    day = timing.get('day', 'monday')
                    if day.lower() == 'monday':
                        schedule.every().monday.at(timing.get('time', '09:00')).do(run_email_notifier)


def run_scheduler():
    """Main scheduler loop"""
    # Simple configuration for demo purposes
    config = {
        'analyzer': {'enabled': True},
        'email_notifier': {'enabled': True}
    }
    
    setup_schedules(config)
    
    logging.info("Scheduler started...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    run_scheduler()