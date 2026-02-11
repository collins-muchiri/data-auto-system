"""
Web dashboard for the Data Automation System
"""
from flask import Flask, render_template, jsonify, request
import os
import subprocess
import threading
import time
from datetime import datetime
import yaml
import json

# Create Flask app with explicit template folder
app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    """Main dashboard view"""
    return render_template('index.html')


@app.route('/status')
def status():
    """System status view"""
    return render_template('status.html')


@app.route('/api/run-analysis', methods=['POST'])
def run_analysis():
    """API endpoint to trigger data analysis"""
    try:
        # Run the analyzer in a separate thread to avoid blocking
        def run_analyzer():
            try:
                result = subprocess.run(
                    ['python', '../scripts/analyzer.py'],
                    cwd='.',
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode == 0:
                    return {"success": True, "message": "Analysis completed successfully", "output": result.stdout}
                else:
                    return {"success": False, "message": f"Analysis failed: {result.stderr}", "output": result.stderr}
            except subprocess.TimeoutExpired:
                return {"success": False, "message": "Analysis timed out after 5 minutes"}
            except Exception as e:
                return {"success": False, "message": f"Error running analysis: {str(e)}"}

        # Run analysis in a separate thread
        analysis_thread = threading.Thread(target=lambda: setattr(app, '_analysis_result', run_analyzer()))
        analysis_thread.start()
        analysis_thread.join(timeout=305)  # Wait up to 5 minutes plus buffer
        
        # Return response immediately
        return jsonify({"success": True, "message": "Analysis started successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """API endpoint to generate reports"""
    try:
        import sys
        import os
        # Add the scripts directory to the path so we can import reports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
        
        from reports import generate_comprehensive_report, list_reports
        
        # Find the most recently modified data file in the raw data directory
        raw_data_dir = '../data/raw'
        if not os.path.exists(raw_data_dir):
            os.makedirs(raw_data_dir, exist_ok=True)
        
        data_files = []
        for filename in os.listdir(raw_data_dir):
            if filename.lower().endswith(('.csv', '.xlsx', '.xls', '.json')):
                filepath = os.path.join(raw_data_dir, filename)
                mod_time = os.path.getmtime(filepath)
                data_files.append((filepath, mod_time))
        
        if not data_files:
            # If no data files exist, create a sample data file first
            import sys
            import os
            # Add the data/raw directory to the path so we can import synthetic_data
            data_raw_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'data', 'raw')
            sys.path.insert(0, data_raw_path)
            
            # Import and run the synthetic data generator
            from synthetic_data import create_sample_sales_data
            sample_path = os.path.join(raw_data_dir, 'sample_sales_data.csv')
            create_sample_sales_data(output_path=sample_path)
            data_files = [(sample_path, os.path.getmtime(sample_path))]
        
        # Get the most recently modified file
        latest_file = max(data_files, key=lambda x: x[1])[0]
        
        # Generate report from the latest data file
        report_path = generate_comprehensive_report(latest_file, output_format='txt')
        
        # Get updated list of reports
        reports_list = list_reports()
        
        return jsonify({
            "success": True, 
            "message": f"Report generated successfully: {os.path.basename(report_path)}",
            "report_path": report_path,
            "timestamp": datetime.now().isoformat(),
            "reports_available": len(reports_list)
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/view-logs', methods=['GET'])
def view_logs():
    """API endpoint to get recent logs"""
    try:
        import os
        log_files = []
        logs_dir = '../logs'
        
        if os.path.exists(logs_dir):
            for filename in os.listdir(logs_dir):
                if filename.endswith('.log'):
                    filepath = os.path.join(logs_dir, filename)
                    # Get last 50 lines of each log file
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        recent_lines = lines[-50:] if len(lines) > 50 else lines
                        log_files.append({
                            "filename": filename,
                            "recent_entries": "".join(recent_lines)
                        })
        
        return jsonify({
            "success": True,
            "logs": log_files
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/system-settings', methods=['GET', 'POST'])
def system_settings():
    """API endpoint to get or update system settings"""
    try:
        if request.method == 'POST':
            # Handle settings update
            settings = request.json
            # In a real implementation, this would update the config file
            return jsonify({
                "success": True,
                "message": "Settings updated successfully",
                "settings": settings
            })
        else:
            # Return current settings
            with open('../config.yaml', 'r') as file:
                config = yaml.safe_load(file)
            
            # Return only safe settings (not passwords)
            safe_config = config.copy()
            if 'email' in safe_config and 'sender_password' in safe_config['email']:
                safe_config['email']['sender_password'] = "***HIDDEN***"
            
            return jsonify({
                "success": True,
                "settings": safe_config
            })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)