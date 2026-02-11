#!/bin/bash
# Production startup script for Data Auto System

set -e  # Exit on any error

echo "🚀 Starting Data Auto System in Production Mode..."

# Create necessary directories if they don't exist
mkdir -p data/raw data/processed reports logs

# Check if virtual environment exists, if not create it
if [ ! -d "data-auto-system-env" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv data-auto-system-env
fi

# Activate virtual environment
source data-auto-system-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements based on selected mode
case "$1" in
    "streamlit")
        echo "📥 Installing Streamlit requirements..."
        pip install -r requirements-streamlit.txt
        ;;
    *)
        echo "📥 Installing production requirements..."
        pip install -r requirements-production.txt
        ;;
esac

# Run the system
echo "⚙️ Starting system components..."
case "$1" in
    "dashboard")
        echo "🌐 Starting Flask dashboard..."
        cd dashboard && gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app
        ;;
    "streamlit")
        echo "📊 Starting Streamlit dashboard..."
        streamlit run dashboard_streamlit.py --server.port 8501 --server.address 0.0.0.0
        ;;
    "scheduler")
        echo "🕒 Starting scheduler..."
        cd scripts && python scheduler.py
        ;;
    "analyzer")
        echo "🔍 Starting analyzer..."
        cd scripts && python analyzer.py
        ;;
    "all")
        echo "🌟 Starting all components..."
        # In a real production setup, you'd use a process manager like systemd
        # For now, we'll just start the Flask dashboard
        cd dashboard && gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app
        ;;
    *)
        echo "Usage: $0 {dashboard|streamlit|scheduler|analyzer|all}"
        echo "dashboard - Start the Flask web dashboard"
        echo "streamlit - Start the Streamlit analytics dashboard"
        echo "scheduler - Start the task scheduler"
        echo "analyzer - Run the data analyzer"
        echo "all - Start all components (basic implementation)"
        exit 1
        ;;
esac

echo "✅ Data Auto System started successfully!"