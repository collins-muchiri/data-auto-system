# Data Auto System - Production Ready

A comprehensive data automation system with analytics, scheduling, and reporting capabilities.

## 🚀 Features

- **Web Dashboard**: Real-time monitoring and control
- **Automated Analytics**: Process and analyze data files automatically
- **Scheduling**: Cron-like task scheduling
- **Email Notifications**: Status updates and alerts
- **Logging**: Comprehensive system logging
- **Production Ready**: Optimized for deployment

## 📋 Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- Docker Compose (optional)

## 🛠️ Installation

### Option 1: Direct Installation

```bash
# Clone the repository
git clone <repository-url>
cd data-auto-system

# Create virtual environment
python -m venv data-auto-system-env
source data-auto-system-env/bin/activate  # On Windows: data-auto-system-env\Scripts\activate

# Install production requirements
pip install -r requirements-production.txt

# Configure the system
cp config-production.yaml config.yaml
# Edit config.yaml with your specific settings

# Start the system
./start-production.sh dashboard
```

### Option 2: Streamlit Analytics Dashboard

For a simple CSV upload and analytics interface:

```bash
# Install Streamlit requirements
pip install -r requirements-streamlit.txt

# Start the Streamlit dashboard
./start-production.sh streamlit
```

### Option 3: Docker Deployment

```bash
# Build and start the containers
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

## ⚙️ Configuration

### Environment Variables

For production deployments, set these environment variables:

```bash
# Dashboard
DASHBOARD_SECRET_KEY=your-very-secure-secret-key

# Email (for notifications)
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
ADMIN_EMAIL=admin@yourdomain.com

# Hostname (for security)
HOSTNAME=your-domain.com
```

### Configuration File

The system uses `config-production.yaml` for settings. Key sections:

- `system`: Basic system settings
- `dashboard`: Web interface configuration
- `scheduler`: Task scheduling settings
- `email`: Email notification settings
- `paths`: Directory configurations
- `security`: Security-related settings
- `logging`: Logging configuration

## 🖥️ Running the System

### Available Services

```bash
# Start the Flask dashboard
./start-production.sh dashboard

# Start the Streamlit analytics dashboard
./start-production.sh streamlit

# Start the scheduler
./start-production.sh scheduler

# Run the analyzer
./start-production.sh analyzer

# Start all components
./start-production.sh all
```

### Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Scale workers (if needed)
docker-compose up -d --scale app=3
```

## 🔐 Security

- CSRF protection enabled
- Rate limiting implemented
- Secure session handling
- Environment variable-based secrets
- Input validation

## 📊 Monitoring

- Dashboard provides real-time status
- Comprehensive logging to `/app/logs`
- Health check endpoints available
- Email notifications for critical events

## 🔄 Updates

To update the system:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements-production.txt

# Restart services
# For direct installation: restart the services
# For Docker: docker-compose up -d --build
```

## 🛡️ Production Best Practices

1. **Secrets Management**: Use environment variables for sensitive data
2. **SSL/TLS**: Enable SSL in production (update config.yaml)
3. **Reverse Proxy**: Use nginx/Apache as reverse proxy
4. **Database**: Consider using PostgreSQL/MySQL for production
5. **Monitoring**: Set up external monitoring for uptime
6. **Backups**: Regular backups of data and configurations
7. **Firewall**: Restrict access to necessary ports only

## 🆘 Support

For issues and support:

- Check logs in the `logs/` directory
- Review configuration in `config-production.yaml`
- Ensure all dependencies are met
- Verify environment variables are set correctly

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Data Auto System                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Flask         │    │   Streamlit     │    │   Pharma Hub    │        │
│  │   Dashboard     │    │   Dashboard     │    │   Integration   │        │
│  │   (Port 5000)   │    │   (Port 8501)   │    │   (Port 8502)   │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│              │                      │                      │               │
│              ▼                      ▼                      ▼               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Core Components                            │   │
│  ├─────────────────┬─────────────────┬─────────────────┬─────────────┤   │
│  │   Data          │   Analyzer      │   Scheduler     │   Email     │   │
│  │   Processor     │                 │                 │   Notifier  │   │
│  └─────────────────┴─────────────────┴─────────────────┴─────────────┘   │
│              │                      │                      │               │
│              ▼                      ▼                      ▼               │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Raw Data      │    │   Processed     │    │   Reports &     │        │
│  │   Directory     │    │   Data          │    │   Logs          │        │
│  │   (/data/raw)   │    │   (/data/proc)  │    │   (/logs)       │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📈 System Flow

1. **Data Ingestion**: CSV files uploaded via Streamlit or Pharma Hub
2. **Processing**: Data Auto System processes and analyzes data
3. **Storage**: Raw and processed data stored in organized directories
4. **Visualization**: Real-time dashboards display analytics
5. **Automation**: Scheduled tasks run automatically
6. **Notifications**: Email alerts sent for important events
7. **Reporting**: Comprehensive reports generated and stored

## 📋 System Requirements

### Hardware Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 10GB free space for data and logs
- **Network**: Stable internet connection for email notifications

### Software Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **Dependencies**: See requirements files
- **Ports**: 5000 (Flask), 8501 (Streamlit), 8502 (Pharma Hub)

### Runtime Dependencies
- pandas
- numpy
- flask
- streamlit
- plotly
- schedule
- pyyaml
- openpyxl
- xlrd
- requests

## 📁 Directory Structure

```
data-auto-system/
├── README.md                          # Documentation
├── requirements.txt                   # Python dependencies
├── requirements-production.txt        # Production dependencies
├── requirements-streamlit.txt         # Streamlit dependencies
├── config.yaml                        # Configuration file
├── config-production.yaml             # Production configuration
├── run_system.py                      # Main entry point
├── start-production.sh                # Production startup script
├── Dockerfile                         # Container configuration
├── docker-compose.yml                 # Multi-container setup
├── dashboard/                         # Flask dashboard
│   ├── app.py
│   └── templates/
├── dashboard_streamlit.py             # Streamlit dashboard
├── phama.py                           # Pharma Hub integration
├── scripts/                           # Core automation scripts
│   ├── analyzer.py
│   ├── scheduler.py
│   ├── email_notifier.py
│   ├── reports.py
│   └── data/
│       └── raw/
│           └── synthetic_data.py
├── data/                              # Data files
│   ├── raw/
│   └── processed/
├── reports/                           # Generated reports
├── logs/                              # System logs
└── notebooks/                         # Jupyter notebooks
```

## 📄 License

[Specify your license here]