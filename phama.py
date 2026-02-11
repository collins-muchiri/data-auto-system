"""
Pharma Analytics Hub - Integration between Streamlit and Data Auto System
Connects Streamlit dashboard to the Data Auto System for enhanced pharmaceutical analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io
import requests
import json
import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys

# Set up logging
def setup_logging():
    """Set up comprehensive logging for the Pharma Hub"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("./logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("pharma_hub")
    logger.setLevel(logging.DEBUG)
    
    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        logs_dir / "pharma_hub.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = setup_logging()

# Log system startup
logger.info("Pharma Analytics Hub started")

# Set page config
st.set_page_config(
    page_title="Pharma Analytics Hub",
    page_icon="💊",
    layout="wide"
)

# Title
st.title("💊 Pharma Analytics Hub")
st.markdown("Integrated dashboard connecting Streamlit to Data Auto System for enhanced pharmaceutical analytics")

# Log page access
logger.info("Pharma Analytics Hub accessed via web interface")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Home", "Data Upload", "Analytics", "System Integration", "Reports"])

if page == "Home":
    logger.info("User navigated to Home page")
    st.header("Welcome to Pharma Analytics Hub")
    st.markdown("""
    This integrated dashboard combines the ease of Streamlit with the power of the Data Auto System.
    
    **Features:**
    - CSV file upload and instant analytics
    - Connection to Data Auto System backend
    - Advanced pharmaceutical analytics
    - Report generation and sharing
    - Real-time system monitoring
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Streamlit Capabilities")
        st.markdown("""
        - Easy CSV upload
        - Interactive visualizations
        - Real-time analytics
        - User-friendly interface
        """)
    with col2:
        st.subheader("Data Auto System Integration")
        st.markdown("""
        - Advanced analytics
        - Automated reporting
        - Email notifications
        - Scheduled tasks
        """)

elif page == "Data Upload":
    st.header("Data Upload & Processing")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file for pharmaceutical data analysis",
        type="csv",
        help="Upload a CSV file containing pharmaceutical sales or analytics data"
    )
    
    if uploaded_file is not None:
        # Read the CSV file
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded file with {df.shape[0]} rows and {df.shape[1]} columns")
            
            # Store dataframe in session state
            st.session_state.df = df
            
            # Show raw data preview
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Data exploration
            st.subheader("Dataset Overview")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Records", len(df))
            col2.metric("Total Columns", len(df.columns))
            col3.metric("Missing Values", df.isnull().sum().sum())
            col4.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # Identify potential pharmaceutical columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            text_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            # Date column detection
            date_columns = []
            for col in df.columns:
                try:
                    pd.to_datetime(df[col])
                    date_columns.append(col)
                except:
                    continue
            
            st.subheader("Column Analysis")
            col1, col2, col3 = st.columns(3)
            col1.write("**Numeric Columns**")
            col1.write(numeric_columns)
            col2.write("**Text Columns**")
            col2.write(text_columns)
            col3.write("**Date Columns**")
            col3.write(date_columns)
            
            # Button to send data to Data Auto System
            if st.button("Send to Data Auto System for Advanced Analysis"):
                # Save the dataframe to the raw data directory
                data_dir = Path("./data/raw")
                data_dir.mkdir(exist_ok=True)
                
                # Create a unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pharma_upload_{timestamp}.csv"
                filepath = data_dir / filename
                
                df.to_csv(filepath, index=False)
                
                st.success(f"Data saved to {filepath} and sent to Data Auto System")
                
                # Optionally trigger analysis via API
                try:
                    response = requests.post("http://localhost:5000/api/run-analysis", 
                                           json={"file_path": str(filepath)})
                    if response.status_code == 200:
                        st.info("Analysis triggered in Data Auto System")
                    else:
                        st.warning("Could not trigger analysis in Data Auto System")
                except:
                    st.warning("Data Auto System not reachable. File saved locally.")
        
        except Exception as e:
            st.error(f"Error reading the file: {str(e)}")
            st.info("Please make sure your CSV file is properly formatted")

elif page == "Analytics":
    logger.info("User navigated to Analytics page")
    st.header("Advanced Analytics")

    if 'df' in st.session_state:
        logger.info("Loading data for analytics")
        df = st.session_state.df

        # Identify potential sales/quantity columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        if numeric_columns:
            # Select sales/quantity column
            sales_col = st.selectbox("Select Sales/Quantity Column", numeric_columns)
            logger.info(f"User selected sales column: {sales_col}")

            # Select category column if available
            text_columns = df.select_dtypes(include=['object']).columns.tolist()
            category_col = st.selectbox("Select Category/Group Column (optional)", 
                                      ["None"] + text_columns)
            if category_col != "None":
                logger.info(f"User selected category column: {category_col}")

            # Select date column if available
            date_columns = []
            for col in df.columns:
                try:
                    pd.to_datetime(df[col])
                    date_columns.append(col)
                    logger.debug(f"Detected date column: {col}")
                except:
                    continue

            date_col = st.selectbox("Select Date Column (optional)", 
                                   ["None"] + date_columns)
            if date_col != "None":
                logger.info(f"User selected date column: {date_col}")

            # Create analytics
            if sales_col:
                # Basic statistics
                st.subheader("Basic Statistics")
                stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                stats_col1.metric("Total Sales", f"{df[sales_col].sum():,.2f}")
                stats_col2.metric("Average Sale", f"{df[sales_col].mean():,.2f}")
                stats_col3.metric("Max Sale", f"{df[sales_col].max():,.2f}")
                stats_col4.metric("Min Sale", f"{df[sales_col].min():,.2f}")

                # Charts
                st.subheader("Visualizations")

                # Chart 1: Sales distribution histogram
                fig_hist = px.histogram(df, x=sales_col, title=f"Distribution of {sales_col}")
                st.plotly_chart(fig_hist, use_container_width=True)
                logger.info(f"Generated histogram for {sales_col}")

                # Chart 2: Top categories if category column is selected
                if category_col != "None":
                    top_categories = df.groupby(category_col)[sales_col].sum().sort_values(ascending=False).head(10)
                    fig_bar = px.bar(
                        x=top_categories.values,
                        y=top_categories.index,
                        orientation='h',
                        title=f"Top 10 {category_col} by {sales_col}",
                        labels={'x': sales_col, 'y': category_col}
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                    logger.info(f"Generated bar chart for {category_col} by {sales_col}")

                # Chart 3: Time series if date column is selected
                if date_col != "None":
                    try:
                        df[date_col] = pd.to_datetime(df[date_col])
                        df_sorted = df.sort_values(date_col)

                        fig_line = px.line(
                            df_sorted,
                            x=date_col,
                            y=sales_col,
                            title=f"{sales_col} Over Time"
                        )
                        st.plotly_chart(fig_line, use_container_width=True)
                        logger.info(f"Generated time series chart for {sales_col} over {date_col}")
                    except Exception as e:
                        st.warning(f"Could not parse {date_col} as dates for time series chart")
                        logger.warning(f"Error creating time series chart: {str(e)}")

                # Chart 4: Correlation heatmap if multiple numeric columns
                if len(numeric_columns) > 1:
                    corr_df = df[numeric_columns].corr()
                    fig_corr = px.imshow(
                        corr_df,
                        text_auto=True,
                        aspect="auto",
                        title="Correlation Heatmap"
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
                    logger.info("Generated correlation heatmap")
    else:
        st.info("Please upload data in the 'Data Upload' section first")
        logger.info("User tried to access analytics without uploaded data")

elif page == "System Integration":
    logger.info("User navigated to System Integration page")
    st.header("Data Auto System Integration")
    
    st.subheader("System Status")
    
    # Try to connect to the Data Auto System
    try:
        logger.info("Attempting to connect to Data Auto System at http://localhost:5000/status")
        response = requests.get("http://localhost:5000/status", timeout=5)
        if response.status_code == 200:
            st.success("✅ Data Auto System is running and accessible")
            logger.info("Successfully connected to Data Auto System")
            
            # Show system info
            st.subheader("System Information")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("System Status", "Operational")
                st.metric("Dashboard", "Online")
            with col2:
                st.metric("API Endpoint", "Available")
                st.metric("Last Check", datetime.now().strftime("%H:%M:%S"))
                
        else:
            st.error("❌ Data Auto System is not responding")
            logger.warning(f"Data Auto System responded with status code: {response.status_code}")
    except Exception as conn_error:
        st.warning("⚠️ Could not connect to Data Auto System. Is it running on http://localhost:5000?")
        logger.error(f"Could not connect to Data Auto System: {str(conn_error)}")
        st.info("To start the Data Auto System: ./start-production.sh dashboard")
    
    st.subheader("Integration Capabilities")
    
    # Show available API endpoints
    endpoints = [
        {"Endpoint": "/api/run-analysis", "Description": "Trigger data analysis"},
        {"Endpoint": "/api/generate-report", "Description": "Generate reports"},
        {"Endpoint": "/api/get-reports", "Description": "Get list of reports"},
        {"Endpoint": "/api/send-report-email", "Description": "Send reports via email"},
        {"Endpoint": "/api/view-logs", "Description": "View system logs"},
        {"Endpoint": "/api/system-settings", "Description": "Manage system settings"}
    ]
    
    for endpoint in endpoints:
        st.code(f"{endpoint['Endpoint']} - {endpoint['Description']}")
    
    # Button to trigger analysis in Data Auto System
    if st.button("Trigger Analysis in Data Auto System"):
        logger.info("User clicked 'Trigger Analysis in Data Auto System' button")
        try:
            response = requests.post("http://localhost:5000/api/run-analysis", 
                                   json={"trigger": "manual"})
            if response.status_code == 200:
                result = response.json()
                st.success(result.get("message", "Analysis triggered successfully"))
                logger.info(f"Analysis triggered successfully: {result.get('message', 'Analysis triggered successfully')}")
            else:
                st.error("Failed to trigger analysis")
                logger.warning(f"Failed to trigger analysis. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error triggering analysis: {str(e)}")
            logger.error(f"Error triggering analysis: {str(e)}")
    
    # Button to generate report in Data Auto System
    if st.button("Generate Report in Data Auto System"):
        logger.info("User clicked 'Generate Report in Data Auto System' button")
        try:
            response = requests.post("http://localhost:5000/api/generate-report", 
                                   json={"format": "txt"})
            if response.status_code == 200:
                result = response.json()
                st.success(result.get("message", "Report generated successfully"))
                logger.info(f"Report generated successfully: {result.get('message', 'Report generated successfully')}")
            else:
                st.error("Failed to generate report")
                logger.warning(f"Failed to generate report. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            logger.error(f"Error generating report: {str(e)}")

elif page == "Reports":
    logger.info("User navigated to Reports page")
    st.header("Report Generation & Management")
    
    # Try to get reports from Data Auto System
    try:
        logger.info("Attempting to connect to Data Auto System to get reports")
        response = requests.get("http://localhost:5000/api/get-reports", timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                reports = result.get("reports", [])
                logger.info(f"Retrieved {len(reports)} reports from Data Auto System")
                
                st.subheader(f"Available Reports ({len(reports)})")
                
                if reports:
                    for report in reports:
                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            st.write(f"📄 {report['filename']}")
                        with col2:
                            st.write(f"🕒 {datetime.fromisoformat(report['modified']).strftime('%Y-%m-%d %H:%M:%S')}")
                        with col3:
                            # Button to download report
                            report_path = Path(report['path'])
                            if report_path.exists():
                                with open(report_path, 'r') as f:
                                    st.download_button(
                                        label="Download",
                                        data=f.read(),
                                        file_name=report['filename'],
                                        mime="text/plain",
                                        key=report['filename']
                                    )
                                    logger.info(f"User downloaded report: {report['filename']}")
                else:
                    st.info("No reports available. Generate some reports in the Data Auto System.")
                    logger.info("No reports available from Data Auto System")
            else:
                st.error("Could not retrieve reports from Data Auto System")
                logger.error("Could not retrieve reports from Data Auto System")
        else:
            st.warning("Could not connect to Data Auto System for reports")
            logger.warning(f"Could not connect to Data Auto System for reports. Status code: {response.status_code}")
    except Exception as reports_error:
        st.warning("Could not connect to Data Auto System for reports")
        logger.error(f"Error connecting to Data Auto System for reports: {str(reports_error)}")
    
    # Local reports section
    st.subheader("Local Reports")
    reports_dir = Path("./reports")
    if reports_dir.exists():
        local_reports = list(reports_dir.glob("*.txt")) + list(reports_dir.glob("*.json")) + list(reports_dir.glob("*.csv"))
        logger.info(f"Found {len(local_reports)} local reports")
        
        if local_reports:
            for report in local_reports:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📄 {report.name}")
                with col2:
                    st.write(f"🕒 {datetime.fromtimestamp(report.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
                with col3:
                    with open(report, 'r') as f:
                        st.download_button(
                            label="Download",
                            data=f.read(),
                            file_name=report.name,
                            mime="text/plain",
                            key=f"local_{report.name}"
                        )
                        logger.info(f"User downloaded local report: {report.name}")
        else:
            st.info("No local reports found.")
            logger.info("No local reports found in reports directory")
    else:
        st.info("Reports directory does not exist.")
        logger.info("Reports directory does not exist")

# Footer
st.markdown("---")
st.markdown("*Pharma Analytics Hub - Connecting Streamlit to Data Auto System*")

# Log page render completion
logger.info("Pharma Analytics Hub page rendered successfully")