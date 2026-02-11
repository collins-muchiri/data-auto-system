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

### Option 2: Docker Deployment

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
# Start the dashboard
./start-production.sh dashboard

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

## 📄 License

[Specify your license here]