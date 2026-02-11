"""
Web dashboard for the Data Automation System
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Main dashboard view"""
    return render_template('index.html')

@app.route('/status')
def status():
    """System status view"""
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)