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
    """Run the Flask dashboard component"""
    try:
        dashboard_host = config['dashboard']['host']
        dashboard_port = config['dashboard']['port']
        
        # Change to dashboard directory and run the app
        original_dir = os.getcwd()
        os.chdir('dashboard')
        cmd = ['python', 'app.py']
        
        # Set environment variables if needed
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development' if config['dashboard']['debug'] else 'production'
        
        print(f"Starting Flask dashboard on {dashboard_host}:{dashboard_port}")
        subprocess.run(cmd, env=env)
        
        # Return to original directory
        os.chdir(original_dir)
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        
        # Ensure we return to original directory even if there's an error
        os.chdir(original_dir)


def run_streamlit_dashboard(config):
    """Run the Streamlit dashboard component"""
    try:
        # Run the Streamlit dashboard
        original_dir = os.getcwd()
        cmd = ['streamlit', 'run', 'dashboard_streamlit.py', '--server.port', '8501', '--server.address', '0.0.0.0']
        
        print("Starting Streamlit dashboard on port 8501...")
        subprocess.run(cmd)
        
        # Return to original directory
        os.chdir(original_dir)
    except Exception as e:
        print(f"Error starting Streamlit dashboard: {e}")
        
        # Ensure we return to original directory even if there's an error
        os.chdir(original_dir)


def run_pharma_hub(config):
    """Run the Pharma Hub integration dashboard"""
    try:
        # Run the Pharma Hub dashboard
        original_dir = os.getcwd()
        cmd = ['streamlit', 'run', 'phama.py', '--server.port', '8502', '--server.address', '0.0.0.0']
        
        print("Starting Pharma Hub dashboard on port 8502...")
        subprocess.run(cmd)
        
        # Return to original directory
        os.chdir(original_dir)
    except Exception as e:
        print(f"Error starting Pharma Hub dashboard: {e}")
        
        # Ensure we return to original directory even if there's an error
        os.chdir(original_dir)


def run_scheduler(config):
    """Run the scheduler component"""
    try:
        # Change to scripts directory and run the scheduler
        original_dir = os.getcwd()
        os.chdir('scripts')
        cmd = ['python', 'scheduler.py']
        
        print("Starting scheduler...")
        subprocess.run(cmd)
        
        # Return to original directory
        os.chdir(original_dir)
    except Exception as e:
        print(f"Error starting scheduler: {e}")
        
        # Ensure we return to original directory even if there's an error
        os.chdir(original_dir)


def run_standalone_analyzer(config):
    """Run just the analyzer component"""
    try:
        original_dir = os.getcwd()
        os.chdir('scripts')
        cmd = ['python', 'analyzer.py']
        
        print("Running data analyzer...")
        subprocess.run(cmd)
        
        # Return to original directory
        os.chdir(original_dir)
    except Exception as e:
        print(f"Error running analyzer: {e}")
        
        # Ensure we return to original directory even if there's an error
        os.chdir(original_dir)


def run_all_modules(config):
    """Run all modules simultaneously in separate threads"""
    print("Starting all Data Automation System components...")
    
    # Initialize directories first
    initialize_directories(config)
    
    # Create threads for each component
    threads = []
    
    # Start Flask dashboard
    dashboard_thread = threading.Thread(target=run_dashboard, args=(config,))
    threads.append(dashboard_thread)
    
    # Start Streamlit dashboard
    streamlit_thread = threading.Thread(target=run_streamlit_dashboard, args=(config,))
    threads.append(streamlit_thread)
    
    # Start Pharma Hub
    pharma_thread = threading.Thread(target=run_pharma_hub, args=(config,))
    threads.append(pharma_thread)
    
    # Start scheduler
    scheduler_thread = threading.Thread(target=run_scheduler, args=(config,))
    threads.append(scheduler_thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
        time.sleep(2)  # Small delay between starting each component
    
    # Wait for all threads to complete (this will run indefinitely)
    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser(description='Data Automation System')
    parser.add_argument('--component', choices=['all', 'dashboard', 'streamlit', 'pharma', 'scheduler', 'analyzer', 'all-modules'], 
                        default='all', help='Which component(s) to run')
    parser.add_argument('--config', default='config.yaml', 
                        help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    if args.component == 'all':
        print("Starting all Data Automation System components...")
        initialize_directories(config)
        run_dashboard(config)
        
    elif args.component == 'all-modules':
        print("Starting ALL modules simultaneously...")
        run_all_modules(config)
        
    elif args.component == 'dashboard':
        print("Starting Flask dashboard component...")
        initialize_directories(config)
        run_dashboard(config)
        
    elif args.component == 'streamlit':
        print("Starting Streamlit dashboard component...")
        initialize_directories(config)
        run_streamlit_dashboard(config)
        
    elif args.component == 'pharma':
        print("Starting Pharma Hub component...")
        initialize_directories(config)
        run_pharma_hub(config)
        
    elif args.component == 'scheduler':
        print("Starting scheduler component...")
        initialize_directories(config)
        run_scheduler(config)
        
    elif args.component == 'analyzer':
        print("Running standalone analyzer...")
        initialize_directories(config)
        run_standalone_analyzer(config)


if __name__ == "__main__":
    main()