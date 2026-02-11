"""
Data Analyzer Module
Analyzes data files and generates insights
"""
import os
import pandas as pd


def analyze_data(file_path):
    """
    Analyze a data file and return insights
    """
    try:
        # Determine file type and read accordingly
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # Generate basic statistics
        insights = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_summary': df.describe().to_dict()
        }
        
        return insights
    except Exception as e:
        print(f"Error analyzing data: {str(e)}")
        return None


def process_directory(directory_path):
    """
    Process all data files in a directory
    """
    results = {}
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.csv', '.xlsx', '.xls')):
            file_path = os.path.join(directory_path, filename)
            print(f"Analyzing {file_path}...")
            results[filename] = analyze_data(file_path)
    
    return results


if __name__ == "__main__":
    # Example usage
    raw_data_dir = "../data/raw"
    results = process_directory(raw_data_dir)
    print("Analysis complete!")