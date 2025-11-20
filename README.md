# WHO Alcohol Analysis - Streamlit Dashboard

## 🎯 Streamlined Bilingual Application (English/French)

### Features
- ✅ **Streamlit-only** dashboard (no Dash, no matplotlib)
- ✅ **Bilingual interface** (English/French language switcher)
- ✅ **Live data loading** from WHO API
- ✅ **Interactive visualizations** with Plotly
- ✅ **Export to HTML** report on demand
- ✅ **Clean architecture** - removed all unused plotting code

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run streamlit_app.py
```

The dashboard will open at: `http://localhost:8501`

### Project Structure

```
├── streamlit_app.py           # Main Streamlit application
├── requirements.txt           # Dependencies (Streamlit + essentials)
├── config/
│   ├── settings.py           # API endpoints & constants
│   └── translations.py       # Bilingual translations (EN/FR)
└── core/
    ├── data_processor.py     # WHO API data fetching
    └── report_generator.py   # HTML report export
```

### Usage

1. **Select Language**: Choose English 🇬🇧 or French 🇫🇷 in sidebar
2. **Load Data**: Click "Load WHO Data" button
3. **Explore**: Navigate through 6 tabs:
   - 📊 Overview
   - 🍷 Consumption
   - 🏥 Disorders
   - 🔗 Correlations
   - 🌍 Regional
   - 📄 Export
4. **Export**: Go to Export tab, generate full HTML report

### Key Differences from Original

**Removed:**
- ❌ Dash framework dependencies
- ❌ Matplotlib/Seaborn static plots
- ❌ Suicide data (limited API availability)
- ❌ Former drinkers data (limited coverage)
- ❌ Clustering analysis
- ❌ Command-line modes
- ❌ Auto-generation on startup

**Kept:**
- ✅ Core WHO data (consumption + disorders)
- ✅ All essential visualizations
- ✅ Correlation analysis
- ✅ Regional comparisons
- ✅ Europe trends
- ✅ HTML report generation

**Added:**
- ✅ Complete bilingual support
- ✅ User-triggered data loading
- ✅ On-demand report generation
- ✅ Clean Streamlit-native interface

### Data Sources

- **WHO Global Health Observatory**
- Alcohol Consumption: SA_0000001747
- Alcohol Use Disorders: SA_0000001462

### Technologies

- Streamlit 1.28+
- Plotly 5.0+
- Pandas 1.5+
- WHO GHO OData API
