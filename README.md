# 📊 Data Auto System

**A Complete, Portable Data Analysis & Automation Platform**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)](https://streamlit.io)

Turn complex data analysis into simple, one-click automation. No coding required.

---

## 🎯 What Problem Does This Solve?

**Stop wasting time on manual data tasks.** This system solves:

- ✅ **Technical barriers** - No coding skills needed
- ✅ **Time-consuming reporting** - Automated analysis in seconds  
- ✅ **Inconsistent metrics** - Standardized analysis every time
- ✅ **Manual email distribution** - Automated report delivery
- ✅ **Limited accessibility** - Anyone can generate insights

**Perfect for:** Small businesses, sales teams, marketing departments, freelancers, students, and anyone who works with data.

---

## 🚀 Quick Start (3 Minutes)

### For Non-Technical Users:
```bash
# 1. Download and extract the folder
# 2. Double-click 'start_dashboard.bat' (Windows) or './start_dashboard.sh' (Mac/Linux)
# 3. Open your browser to http://localhost:8501
# 4. Upload your CSV file and click "Run Analysis"
```

### For Technical Users:
```bash
# 1. Clone or download this repository
git clone https://github.com/[USERNAME]/data-auto-system.git
cd data-auto-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the system
python run_system.py --component all
```

---

## 📁 System Overview

```
data-auto-system/
├── 📊 dashboard/           # Web interface (Flask)
├── 📊 dashboard_streamlit.py  # Streamlit dashboard
├── 📊 phama.py           # Pharma Hub integration
├── ⚙️ scripts/             # Core automation logic
├── 📁 data/               # Input/output data folders
├── 📄 reports/           # Generated reports & charts
├── 🐍 notebooks/         # Jupyter notebooks for advanced analysis
├── 🔧 config.yaml         # System configuration
├── 🔧 config-production.yaml # Production configuration
├── 📋 requirements.txt    # Python dependencies
├── 📋 requirements-streamlit.txt # Streamlit dependencies
├── 📋 requirements-production.txt # Production dependencies
├── 🚀 run_system.py      # Main entry point
└── 🚀 start-production.sh # Production startup script
```

---

## 🔧 Features

### 🖥️ **Web Dashboard**
- Drag-and-drop file upload
- Instant data preview
- Interactive charts and visualizations
- One-click analysis
- Downloadable reports

### ⚡ **Automation**
- Scheduled reports (daily/weekly/monthly)
- Automated email notifications
- Background task processing
- Error handling and logging

### 📈 **Analysis Capabilities**
- Sales trend analysis
- Customer segmentation (RFM)
- Product performance ranking
- Revenue forecasting
- Data quality checks

### 📧 **Notifications**
- Email reports with attachments
- Customizable recipients
- SMTP integration (Gmail, Outlook, Mailtrap)
- Error alerts

---

## 🎮 How to Use

### Method 1: Web Interface (Recommended)
1. **Start dashboard**: `python run_system.py --mode dashboard`
2. **Upload CSV**: Use the file uploader in the web interface
3. **View results**: Instant charts, statistics, and insights
4. **Download reports**: Export as PDF, CSV, or Excel

### Method 2: Automated Scheduling
1. **Configure schedule**: Edit `config.yaml`
2. **Add your data**: Place files in `data/raw/`
3. **Start scheduler**: `python run_system.py --mode scheduler`
4. **System runs automatically** according to your schedule

### Method 3: Command Line
```bash
# One-time analysis
python run_system.py --mode analyze

# Custom dataset
python run_system.py --mode analyze --file your_data.csv

# With email notifications
python run_system.py --mode analyze --email
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
system:
  name: "Your Company Analytics"
  
email:
  enabled: true
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "your-email@gmail.com"
  sender_password: "your-app-password"  # Use App Password for Gmail
  recipients: ["team@company.com"]
  
analysis:
  default_dataset: "sales_data.csv"
  auto_run: true
  schedule: "daily"  # daily, weekly, monthly
  
logging:
  level: "INFO"
  file: "logs/system.log"
```

### Email Setup Guide:
1. **Gmail**: Enable 2FA and generate App Password
2. **Outlook**: Use your regular password
3. **Mailtrap**: Free testing service (no real emails sent)
4. **Other SMTP providers**: Configure with your provider's settings

---

## 📊 Supported Data Formats

### Input:
- ✅ CSV files (.csv)
- ✅ Excel files (.xlsx, .xls)
- ✅ JSON data (.json)

### Expected Columns (automatically detected):
```
InvoiceNo, StockCode, Description, Quantity, 
InvoiceDate, UnitPrice, CustomerID, Country,
Sales, Revenue, Amount, Date, Product, Customer
```

### Sample Data Structure:
```csv
InvoiceNo,Description,Quantity,UnitPrice,CustomerID,Country,InvoiceDate
INV001,Product A,2,25.00,17850,United Kingdom,2024-01-01 10:00:00
INV002,Product B,1,15.00,13047,Germany,2024-01-01 11:30:00
```

---

## 🎪 Use Cases

### Small Business Owner:
_"I upload my daily sales CSV and get instant profit analysis emailed to me every morning."_

### Sales Team:
_"We track campaign performance with automated weekly reports sent to the entire team."_

### Marketing Manager:
_"I analyze customer behavior patterns to optimize our advertising spend."_

### Student/Researcher:
_"I process research data without learning complex statistical software."_

### Freelancer:
_"I automate client reporting, saving hours each week on manual work."_

---

## 🛠️ Technical Details

### Requirements:
- Python 3.7+
- 4GB RAM recommended
- 500MB disk space

### Dependencies:
```txt
pandas>=2.0.0      # Data manipulation
matplotlib>=3.7.0   # Visualization
seaborn>=0.12.0    # Statistical charts
streamlit>=1.28.0   # Web interface
schedule>=1.2.0     # Task scheduling
pyyaml>=6.0        # Configuration
```

### Architecture:
- **Modular design** - Easy to extend
- **Error handling** - Robust and reliable
- **Logging** - Full audit trail
- **Portable** - Runs anywhere Python runs

---

## 🔍 Advanced Features

### Custom Analysis:
```python
from scripts.analyzer import DataAnalyzer

# Custom analysis pipeline
analyzer = DataAnalyzer()
df = analyzer.load_dataset("your_data.csv")
results = analyzer.sales_analysis(df)
custom_report = analyzer.generate_custom_report(results)
```

### Integration:
```python
# Use as a Python module
import data_auto_system

# API endpoints for web apps
# Database connectors available
# Custom visualization templates
```

### Extensions:
- Add new analysis modules
- Custom data connectors
- Advanced machine learning
- Real-time data streaming

---

## 🐛 Troubleshooting

### Common Issues:

**Email not sending:**
```bash
# Test email configuration
python scripts/email_test.py

# Check logs
tail -f logs/system.log
```

**Dependencies issues:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install individually
pip install pandas matplotlib streamlit
```

**File upload problems:**
- Ensure CSV format is correct
- Check file encoding (use UTF-8)
- Verify column names match expected format

### Getting Help:
1. Check the `logs/system.log` file
2. Run diagnostic: `python diagnose_system.py`
3. Check GitHub Issues for similar problems
4. Contact support with error messages

---

## 📈 Sample Output

### Reports Generated:
- 📊 **Sales Trend Analysis** - Daily/Weekly/Monthly trends
- 🏆 **Top Products** - Revenue ranking and performance
- 👥 **Customer Insights** - RFM segmentation
- 📉 **Performance Metrics** - Key business indicators
- 🔍 **Data Quality Report** - Missing values and anomalies

### Visualizations:
- Line charts for trends
- Bar charts for rankings
- Pie charts for proportions
- Heatmaps for correlations

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Report bugs** - Open an issue with details
2. **Suggest features** - What would make this better for you?
3. **Submit pull requests** - Code improvements welcome
4. **Improve documentation** - Help others get started

### Development Setup:
```bash
git clone https://github.com/[USERNAME]/data-auto-system.git
cd data-auto-system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Attribution:
Please attribute if you use this system in your projects or publications.

---

## 🙋‍♂️ Support

**Need help?**
- 📚 Check the [Wiki](https://github.com/[USERNAME]/data-auto-system/wiki)
- 🐛 [Report an Issue](https://github.com/[USERNAME]/data-auto-system/issues)
- 💬 [Discussion Forum](https://github.com/[USERNAME]/data-auto-system/discussions)

---

## 🚀 Ready to Start?

**Download now and transform your data workflow today!**

---
*Data Auto System - Making data analytics accessible to everyone* 🎯

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.