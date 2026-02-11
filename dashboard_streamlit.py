import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io

# Set page config
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales Analytics Dashboard")
st.markdown("Upload your CSV file to instantly see sales analytics with interactive charts")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type="csv",
    help="Upload a CSV file containing sales data"
)

if uploaded_file is not None:
    # Read the CSV file
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"Successfully loaded file with {df.shape[0]} rows and {df.shape[1]} columns")
        
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
        
        # Identify potential sales columns
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
        
        # Sales analytics dashboard
        st.subheader("Sales Analytics Dashboard")
        
        # If we have numeric columns, create sales analytics
        if numeric_columns:
            # Select sales/quantity column
            sales_col = st.selectbox("Select Sales/Quantity Column", numeric_columns)
            
            # Select category column if available
            category_col = st.selectbox("Select Category/Group Column (optional)", 
                                      ["None"] + text_columns)
            
            # Select date column if available
            date_col = st.selectbox("Select Date Column (optional)", 
                                   ["None"] + date_columns)
            
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
                    except:
                        st.warning(f"Could not parse {date_col} as dates for time series chart")
                
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
        
        # Data quality report
        st.subheader("Data Quality Report")
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df)) * 100
        quality_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Missing Percentage': missing_percent.values
        }).round(2)
        
        st.dataframe(quality_df)
        
        # Download processed data
        st.subheader("Download Processed Data")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()
        
        st.download_button(
            label="Download CSV",
            data=csv_string,
            file_name="processed_data.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")
        st.info("Please make sure your CSV file is properly formatted")

else:
    st.info("👆 Please upload a CSV file to begin analysis")

# Footer
st.markdown("---")
st.markdown("*Sales Analytics Dashboard - Upload CSV files to instantly visualize your sales data*")