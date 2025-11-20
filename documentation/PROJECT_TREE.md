# Project Structure - Visual Tree

```
who_alcohol_streamlit/
│
├── 🚀 Main Application
│   └── streamlit_app.py              (450 lines - 6 tabs, bilingual UI)
│
├── ⚙️ Configuration
│   ├── config/__init__.py
│   ├── config/settings.py            (60 lines - API endpoints, constants)
│   └── config/translations.py        (150 lines - EN/FR dictionaries)
│
├── 🔧 Core Functionality
│   ├── core/__init__.py
│   ├── core/data_processor.py        (180 lines - WHO API calls)
│   └── core/report_generator.py      (120 lines - HTML generation)
│
├── 📦 Dependencies
│   └── requirements.txt              (6 packages)
│
├── 🛠️ Utilities
│   ├── verify_setup.py               (Setup checker)
│   └── launch.sh                     (Quick launcher)
│
└── 📖 Documentation
    ├── README.md                     (Main docs)
    ├── QUICKSTART.md                 (2-min guide)
    ├── ARCHITECTURE.md               (System design)
    ├── MIGRATION_GUIDE.md            (Old vs New)
    └── PROJECT_SUMMARY.md            (Complete overview)
```

## File Purposes

### streamlit_app.py
```python
Main UI with 6 tabs:
├─ Sidebar
│  ├─ Language selector (EN/FR)
│  └─ Load Data button
│
└─ Tabs
   ├─ 📊 Overview: Metrics + regional chart
   ├─ 🍷 Consumption: Top 10, map, trends
   ├─ 🏥 Disorders: Gender comparison
   ├─ 🔗 Correlations: R² analysis
   ├─ 🌍 Regional: Tables + charts
   └─ 📄 Export: Generate HTML report
```

### data_processor.py
```python
WHO API Integration:
├─ fetch_alcohol_consumption()   → 2000-2022 data
├─ fetch_alcohol_disorder()      → Gender-specific
├─ merge_consumption_disorder()  → Combined dataset
├─ get_top_consumers()           → Top N countries
├─ get_regional_averages()       → WHO regions
└─ get_europe_trend_data()       → EU trends
```

### report_generator.py
```python
HTML Export:
├─ calculate_stats()       → Key metrics
├─ generate_report()       → Full HTML
└─ Bilingual templates     → EN/FR support
```

### translations.py
```python
Bilingual Support:
TRANSLATIONS = {
    'en': {...},  # English strings
    'fr': {...}   # French strings
}
```

### settings.py
```python
Configuration:
├─ WHO_API_BASE_URL
├─ ALCOHOL_CONSUMPTION_INDICATOR
├─ ALCOHOL_DISORDER_INDICATOR
├─ EU_PRE_1986 countries
├─ COUNTRY_NAME_MAPPING
├─ GENDER_MAPPING
└─ REGION_COLORS
```

## Code Statistics

| File | Lines | Purpose |
|------|-------|---------|
| streamlit_app.py | 450 | Main UI |
| data_processor.py | 180 | API calls |
| translations.py | 150 | EN/FR text |
| report_generator.py | 120 | HTML export |
| settings.py | 60 | Config |
| **TOTAL** | **~800** | **Complete app** |

## Dependencies (6 packages)

```
streamlit  ────► UI framework
pandas     ────► Data manipulation
plotly     ────► Interactive charts
requests   ────► WHO API calls
scipy      ────► Statistics (R²)
numpy      ────► Numerical operations (implicit)
```

## Data Flow

```
WHO API
  │
  ├─► Consumption (SA_0000001747)
  │   └─► Countries × Years (2000-2022)
  │
  ├─► Disorders (SA_0000001462)
  │   └─► Countries × Gender
  │
  ▼
data_processor.py
  │
  ├─► Process & merge
  ├─► Calculate stats
  └─► Generate datasets
  │
  ▼
streamlit_app.py
  │
  ├─► Display in tabs
  ├─► Create charts
  └─► Export reports
  │
  ▼
report_generator.py
  │
  └─► HTML file (bilingual)
```

## User Journey

```
1. Open Dashboard
   └─► streamlit run streamlit_app.py

2. Select Language
   └─► Sidebar: EN 🇬🇧 or FR 🇫🇷

3. Load Data
   └─► Click "Load WHO Data"
   └─► ~10 seconds

4. Explore Tabs
   ├─► Overview: Metrics
   ├─► Consumption: Charts
   ├─► Disorders: Analysis
   ├─► Correlations: R²
   ├─► Regional: Tables
   └─► Export: Generate report

5. Download Report
   └─► Full HTML with all charts
```

## Memory Usage

```
Startup:        ~100MB  (Streamlit + libs)
After load:     ~200MB  (Data cached)
Per tab:        +10MB   (Charts rendered)
Max:            ~300MB  (All tabs visited)
```

## Development vs Production

```
Development:
├─ streamlit run streamlit_app.py
└─ Auto-reload on changes

Production:
├─ Streamlit Cloud deployment
├─ Docker container
└─ Behind nginx proxy
```

## File Size Distribution

```
Code:           ~50 KB
Documentation:  ~80 KB
Total:          ~130 KB (ultra-lightweight!)
```
