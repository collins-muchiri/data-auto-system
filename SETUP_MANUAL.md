# Data Auto System - Setup and Operation Manual

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Project Dependencies](#project-dependencies)
5. [Configuration](#configuration)
6. [Running the System](#running-the-system)
7. [Generating Sample Data](#generating-sample-data)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Troubleshooting](#troubleshooting)

## Overview

The Data Auto System is an automated system for processing, analyzing, and reporting on data workflows. It includes components for data analysis, scheduling, email notifications, and a web dashboard for monitoring.

## Prerequisites

Before setting up the system, ensure you have:

- Python 3.7 or higher
- pip package manager
- Git (optional, for cloning the repository)

## Environment Setup

### Step 1: Clone or Access the Project

Navigate to your project directory:
```bash
cd c:\Users\Muchi\Desktop\Projects\data-auto-systems
```

### Step 2: Create a Virtual Environment

Create a virtual environment to isolate the project dependencies:

**On Windows:**
```bash
python -m venv data-auto-system-env
```

This creates a virtual environment in the `data-auto-system-env` directory.

### Step 3: Activate the Virtual Environment

**On Windows:**
```bash
data-auto-system-env\Scripts\activate
```

After activation, your command prompt should show `(data-auto-system-env)` at the beginning of the line.

### Step 4: Verify Virtual Environment Activation

Check that you're using the virtual environment's Python:
```bash
where python
```

This should show the Python executable from your virtual environment directory.

## Project Dependencies

### Step 1: Install Required Packages

With the virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

If you encounter issues with the requirements file, you can install the packages manually:

```bash
pip install pandas numpy flask schedule pyyaml openpyxl xlrd requests
```

### Step 2: Verify Installation

Check that the packages are installed correctly:

```bash
pip list
```

Look for the required packages in the list.

## Configuration

### Step 1: Review Configuration File

The system uses `config.yaml` for configuration. Open this file to review and adjust settings:

```yaml
# Configuration for Data Automation System

system:
  name: "Data Auto System"
  version: "1.0.0"
  debug: false

dashboard:
  host: "0.0.0.0"
  port: 5000
  debug: false

scheduler:
  enabled: true
  timezone: "UTC"
  tasks:
    analyzer:
      enabled: true
      schedule: "0 2 * * *"  # Daily at 2 AM
    email_notifier:
      enabled: true
      schedule: "0 9 * * 1"  # Weekly on Monday at 9 AM

email:
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "your_email@gmail.com"
  sender_password: "your_app_password"

paths:
  raw_data_dir: "./data/raw"
  processed_data_dir: "./data/processed"
  reports_dir: "./reports"
  logs_dir: "./logs"

data_processing:
  supported_formats:
    - ".csv"
    - ".xlsx"
    - ".xls"
  auto_clean_raw: false
  backup_processed: true
```

### Step 2: Customize Configuration (Optional)

Modify the `config.yaml` file to match your specific requirements:
- Update email settings if you plan to use email notifications
- Adjust paths if needed
- Modify scheduler settings as required

### Step 3: Email Configuration Options

The system supports multiple email configuration options:

#### Option A: Using Gmail (Production)
1. Use your Gmail address as `sender_email`
2. Generate an App Password in Google Account settings (not your regular password)
3. Update the config with:
   ```yaml
   email:
     smtp_server: "smtp.gmail.com"
     smtp_port: 587
     sender_email: "your_actual_gmail@gmail.com"
     sender_password: "your_app_password_here"
   ```

#### Option B: Using Outlook/Hotmail
1. Use your Outlook/Hotmail address as `sender_email`
2. Update the config with:
   ```yaml
   email:
     smtp_server: "smtp-mail.outlook.com"
     smtp_port: 587
     sender_email: "your_outlook_address@outlook.com"
     sender_password: "your_password"
   ```

#### Option C: Using Local SMTP Server (Development/Test)
For development purposes, Python provides a built-in SMTP debugging server:

1. Open a new command prompt window and navigate to your project directory
2. Run the local SMTP server:
   ```bash
   python -m smtpd -c DebuggingServer -n localhost:1025
   ```
3. Update the config with:
   ```yaml
   email:
     smtp_server: "localhost"
     smtp_port: 1025
     sender_email: "test@example.com"
     sender_password: ""  # Empty for local server
   ```
4. The local server will print emails to the console instead of sending them

#### Option D: Using Mailtrap.io (Testing)
Mailtrap provides a fake SMTP server for testing:

1. Sign up at https://mailtrap.io
2. Get your SMTP credentials from the demo inbox
3. Update the config with:
   ```yaml
   email:
     smtp_server: "smtp.mailtrap.io"
     smtp_port: 587  # or 2525
     sender_email: "your_mailtrap_username"
     sender_password: "your_mailtrap_password"
   ```
4. Emails will be captured in your Mailtrap inbox instead of being sent

## Running the System

### System Architecture Overview

The Data Auto System consists of several interconnected components:

1. **Dashboard** (`dashboard/app.py`) - Web interface for monitoring
2. **Scheduler** (`scripts/scheduler.py`) - Manages automated tasks
3. **Analyzer** (`scripts/analyzer.py`) - Processes and analyzes data
4. **Email Notifier** (`scripts/email_notifier.py`) - Sends notifications
5. **Synthetic Data Generator** (`scripts/data/raw/synthetic_data.py`) - Creates sample data

### Method 1: Run the Complete System

To run all components of the system:

```bash
python run_system.py
```

This will initialize directories and start the dashboard component.

### Method 2: Run Specific Components

#### Run the Dashboard Only
```bash
cd dashboard
python app.py
```
The dashboard will be accessible at `http://localhost:5000`

#### Run the Scheduler Only
```bash
cd scripts
python scheduler.py
```

#### Run the Analyzer Only
```bash
cd scripts
python analyzer.py
```

#### Run the Email Notifier Only
```bash
cd scripts
python email_notifier.py
```

#### Generate Sample Data
```bash
cd scripts\data\raw
python synthetic_data.py
```

#### Test Mailtrap Configuration
```bash
python test_mailtrap.py
```

### Method 3: Run with Arguments

You can specify which component to run:

```bash
# Run all components
python run_system.py --component all

# Run only the dashboard
python run_system.py --component dashboard

# Run only the scheduler
python run_system.py --component scheduler

# Run only the analyzer
python run_system.py --component analyzer
```

### Method 4: Component-Specific Operations

#### Analyze Specific Data File
```bash
cd scripts
python analyzer.py  # This will analyze files in the data/raw directory
```

#### Run Scheduler with Custom Config
```bash
cd scripts
python scheduler.py  # Uses config from parent config.yaml
```

### Recommended Startup Sequence

For a complete system test, follow this sequence:

1. Generate sample data:
   ```bash
   cd scripts\data\raw
   python synthetic_data.py
   ```

2. Test email configuration (optional):
   ```bash
   python test_mailtrap.py
   ```

3. Start the dashboard:
   ```bash
   cd ../..  # Back to main project directory
   python run_system.py --component dashboard
   ```

4. In a separate terminal, start the scheduler:
   ```bash
   cd scripts
   python scheduler.py
   ```

### Running with Different Environments

#### Development Mode
For development, you might want to run components separately to see detailed logs:

1. Terminal 1 - Dashboard: `python run_system.py --component dashboard`
2. Terminal 2 - Scheduler: `cd scripts && python scheduler.py`
3. Terminal 3 - Monitor logs: `tail -f logs/*.log`

#### Production Mode
For production deployment, consider using process managers like systemd (Linux) or NSSM (Windows) to keep services running.

## Generating Sample Data

### Step 1: Navigate to the Synthetic Data Script

The synthetic data generator is located at:
`c:\Users\Muchi\Desktop\Projects\data-auto-systems\scripts\data\raw\synthetic_data.py`

### Step 2: Run the Synthetic Data Generator

With the virtual environment activated:

```bash
cd scripts\data\raw
python synthetic_data.py
```

This will create a sample sales dataset with 1000 rows in the `data/raw` directory named `sample_sales_data.csv`.

### Step 3: Verify Sample Data Creation

Check that the file was created:
- Path: `c:\Users\Muchi\Desktop\Projects\data-auto-systems\data\raw\sample_sales_data.csv`
- The script will output information about the created dataset

## Monitoring and Logging

### Log Files Location

The system creates log files in the `logs` directory:
- `scheduler.log` - Logs from the scheduler component
- `email_notifier.log` - Logs from the email notification component

### Dashboard Monitoring

Access the dashboard at `http://localhost:5000` to monitor system status (when running).

## Troubleshooting

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError" when running scripts
**Solution:** Ensure your virtual environment is activated and dependencies are installed:
```bash
# Activate virtual environment
data-auto-system-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Issue: Permission errors when creating directories/files
**Solution:** Ensure you have write permissions to the project directory and run your command prompt as administrator if needed.

#### Issue: Port already in use when starting dashboard
**Solution:** Check if another process is using port 5000:
```bash
netstat -ano | findstr :5000
```
Terminate the conflicting process or change the port in `config.yaml`.

#### Issue: Email notifications not working
**Solution:**
1. Verify email settings in `config.yaml`
2. For Gmail, ensure "App Passwords" are used instead of the regular password
3. Check firewall settings
4. If using a local SMTP server, ensure it's running with: `python -m smtpd -c DebuggingServer -n localhost:1025`
5. If using a test service like Mailtrap, verify your credentials are correct

### Verifying System Health

1. Check that all required directories exist:
   - `data/raw`
   - `data/processed`
   - `reports`
   - `logs`
   - `dashboard/templates`

2. Verify that dependencies are installed:
```bash
pip list
```

3. Check log files in the `logs` directory for any errors.

### Deactivating the Virtual Environment

When you're done working with the system, deactivate the virtual environment:

```bash
deactivate
```

## Next Steps

Once your system is running:

1. Generate sample data using the synthetic data generator
2. Access the dashboard to monitor system status
3. Configure email notifications if needed (see Email Configuration Options in Configuration section)
4. Set up scheduled tasks according to your requirements
5. Add your own data files to the `data/raw` directory for processing

For more information about specific components, refer to the individual module documentation in their respective files.

## Setting Up Email Notifications

If you want to enable email notifications, you have several options:

1. **Local Development**: Use Python's built-in SMTP debugging server for testing
2. **Gmail**: Configure with your Gmail account and App Password
3. **Outlook/Hotmail**: Use your Microsoft email account
4. **Mailtrap**: Use for testing without sending real emails

Follow the instructions in the "Email Configuration Options" section to set up your preferred email service.