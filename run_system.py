#!/usr/bin/env python3
"""
Main entry point for the Data Automation System
This script initializes and runs all components of the system
"""

import os
import sys
import yaml
import argparse
import subprocess
import threading
import time
from pathlib import Path


def load_config(config_path="config.yaml"):
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file: {e}")
        sys.exit(1)


def initialize_directories(config):
    """Create required directories if they don't exist"""
    dirs_to_create = [
        config['paths']['raw_data_dir'],
        config['paths']['processed_data_dir'],
        config['paths']['reports_dir'],
        config['paths']['logs_dir']
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Ensured directory exists: {dir_path}")


def run_dashboard(config):
    """Run the dashboard component"""
    try:
        dashboard_host = config['dashboard']['host']
        dashboard_port = config['dashboard']['port']
        
        # Change to dashboard directory and run the app
        os.chdir('dashboard')
        cmd = ['python', 'app.py']
        
        # Set environment variables if needed
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development' if config['dashboard']['debug'] else 'production'
        
        print(f"Starting dashboard on {dashboard_host}:{dashboard_port}")
        subprocess.run(cmd, env=env)
    except Exception as e:
        print(f"Error starting dashboard: {e}")


def run_scheduler(config):
    """Run the scheduler component"""
    try:
        # Change to scripts directory and run the scheduler
        os.chdir('scripts')
        cmd = ['python', 'scheduler.py']
        
        print("Starting scheduler...")
        subprocess.run(cmd)
    except Exception as e:
        print(f"Error starting scheduler: {e}")


def run_standalone_analyzer(config):
    """Run just the analyzer component"""
    try:
        os.chdir('scripts')
        cmd = ['python', 'analyzer.py']
        
        print("Running data analyzer...")
        subprocess.run(cmd)
    except Exception as e:
        print(f"Error running analyzer: {e}")


def main():
    parser = argparse.ArgumentParser(description='Data Automation System')
    parser.add_argument('--component', choices=['all', 'dashboard', 'scheduler', 'analyzer'], 
                        default='all', help='Which component(s) to run')
    parser.add_argument('--config', default='config.yaml', 
                        help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize required directories
    initialize_directories(config)
    
    if args.component == 'all':
        print("Starting all Data Automation System components...")
        
        # Note: In a real implementation, you'd want to run these as separate threads/processes
        # For simplicity, we'll run the dashboard which will internally handle other components
        run_dashboard(config)
        
    elif args.component == 'dashboard':
        print("Starting dashboard component...")
        run_dashboard(config)
        
    elif args.component == 'scheduler':
        print("Starting scheduler component...")
        run_scheduler(config)
        
    elif args.component == 'analyzer':
        print("Running standalone analyzer...")
        run_standalone_analyzer(config)


if __name__ == "__main__":
    main()