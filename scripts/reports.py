"""
Report Generation Module
Generates comprehensive reports from data analysis results
"""
import os
import pandas as pd
import json
from datetime import datetime
from pathlib import Path


def generate_report_from_insights(insights, report_format='txt'):
    """
    Generate a report from analysis insights
    
    Args:
        insights (dict): Insights from data analysis
        report_format (str): Format of the report ('txt', 'json', 'csv')
    
    Returns:
        str: Path to the generated report file
    """
    import os
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Use absolute path based on the project root
    project_root = Path(__file__).parent.parent  # Go up from scripts to project root
    reports_dir = project_root / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    if report_format.lower() == 'json':
        report_filename = f"report_{timestamp}.json"
        report_path = reports_dir / report_filename
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'rows': insights.get('shape', [0, 0])[0],
                'columns': insights.get('shape', [0, 0])[1],
                'column_names': insights.get('columns', []),
                'missing_values_total': sum(insights.get('missing_values', {}).values()),
                'numeric_summary': insights.get('numeric_summary', {})
            }
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
    
    elif report_format.lower() == 'csv':
        # Convert insights to a DataFrame for CSV export
        report_filename = f"report_{timestamp}.csv"
        report_path = reports_dir / report_filename
        
        # Create a summary DataFrame
        summary_data = {
            'Metric': ['Rows', 'Columns', 'Missing Values Total'],
            'Value': [
                insights.get('shape', [0, 0])[0],
                insights.get('shape', [0, 0])[1],
                sum(insights.get('missing_values', {}).values())
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(report_path, index=False)
    
    else:  # Default to text format
        report_filename = f"report_{timestamp}.txt"
        report_path = reports_dir / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"Data Analysis Report\n")
            f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            
            f.write("Dataset Summary:\n")
            f.write(f"  Shape: {insights.get('shape', (0, 0))}\n")
            f.write(f"  Columns: {', '.join(insights.get('columns', []))}\n\n")
            
            f.write("Missing Values:\n")
            for col, count in insights.get('missing_values', {}).items():
                f.write(f"  {col}: {count}\n")
            f.write(f"  Total: {sum(insights.get('missing_values', {}).values())}\n\n")
            
            f.write("Numeric Summary:\n")
            numeric_summary = insights.get('numeric_summary', {})
            for stat, values in numeric_summary.items():
                f.write(f"  {stat}: {values}\n")
    
    return str(report_path)


def generate_comprehensive_report(data_file_path, output_format='txt'):
    """
    Generate a comprehensive report from a data file
    
    Args:
        data_file_path (str): Path to the data file to analyze
        output_format (str): Format of the report ('txt', 'json', 'csv')
    
    Returns:
        str: Path to the generated report file
    """
    import sys
    import os
    # Add the scripts directory to the path so we can import analyzer
    sys.path.insert(0, os.path.dirname(__file__))
    from analyzer import analyze_data
    
    # Analyze the data
    insights = analyze_data(data_file_path)
    
    if insights is None:
        raise ValueError(f"Could not analyze data file: {data_file_path}")
    
    # Generate report from insights
    report_path = generate_report_from_insights(insights, output_format)
    
    return report_path


def list_reports():
    """
    List all generated reports
    
    Returns:
        list: List of report file paths
    """
    import os
    # Use absolute path based on the project root
    project_root = Path(__file__).parent.parent  # Go up from scripts to project root
    reports_dir = project_root / 'reports'
    if not reports_dir.exists():
        return []
    
    report_extensions = ['.txt', '.json', '.csv', '.xlsx', '.pdf']
    reports = []
    
    for file in reports_dir.iterdir():
        if file.is_file() and file.suffix.lower() in report_extensions:
            reports.append({
                'filename': file.name,
                'path': str(file),
                'size': file.stat().st_size,
                'modified': datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    # Sort by modification time (newest first)
    reports.sort(key=lambda x: x['modified'], reverse=True)
    return reports


if __name__ == "__main__":
    # Example usage
    print("Report generation module loaded.")
    print("Use generate_comprehensive_report(data_file_path) to create a report.")