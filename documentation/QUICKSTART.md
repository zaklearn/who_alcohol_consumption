# 🚀 Quick Start Guide

## Installation (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify setup
python verify_setup.py

# 3. Launch dashboard
streamlit run streamlit_app.py
```

Dashboard opens at: `http://localhost:8501`

## First Steps

1. **Select Language** in sidebar: 🇬🇧 English or 🇫🇷 Français
2. **Click "Load WHO Data"** button (takes ~10 seconds)
3. **Explore 6 tabs**:
   - 📊 Overview: Key metrics
   - 🍷 Consumption: Top 10, world map, trends
   - 🏥 Disorders: Gender analysis
   - 🔗 Correlations: R² analysis
   - 🌍 Regional: Averages by region
   - 📄 Export: Generate HTML report

## Features

✅ Bilingual (EN/FR)
✅ Interactive Plotly charts
✅ WHO API data (2000-2022)
✅ Correlation analysis
✅ HTML report export

## Troubleshooting

**Dashboard won't start?**
```bash
pip install --upgrade streamlit
```

**Data loading fails?**
- Check internet connection
- WHO API may be temporarily down

**Import errors?**
```bash
pip install -r requirements.txt --force-reinstall
```

## System Requirements

- Python 3.8+
- Internet connection (for WHO API)
- Modern web browser
- 4GB RAM recommended

## Project Structure

```
├── streamlit_app.py          # Main app
├── config/
│   ├── settings.py           # API config
│   └── translations.py       # EN/FR texts
└── core/
    ├── data_processor.py     # Data fetching
    └── report_generator.py   # HTML export
```

## Support

📖 Full documentation: `README.md`
🏗️ Architecture: `ARCHITECTURE.md`
🔄 Migration guide: `MIGRATION_GUIDE.md`

## Quick Tips

💡 **Data persists** in session - no need to reload between tabs
💡 **Language switch** preserves loaded data
💡 **Reports** are bilingual based on current language
💡 **Charts** are fully interactive - hover, zoom, pan
