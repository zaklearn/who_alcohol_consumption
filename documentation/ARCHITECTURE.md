# Architecture Overview

## New Streamlit-Only Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    streamlit_app.py                         │
│                  (Main Application)                         │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Language   │  │ Data Loading │  │  6 Tabs      │    │
│  │   Selector   │  │   Button     │  │  Navigation  │    │
│  │   (EN/FR)    │  │              │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐
│  translations.py │  │ data_processor.py│  │report_generator│
│  (EN/FR texts)   │  │ (WHO API calls)  │  │   (HTML export)│
└──────────────────┘  └──────────────────┘  └────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   WHO API        │
                    │   - Consumption  │
                    │   - Disorders    │
                    └──────────────────┘
```

## Data Flow

```
User Opens App
    │
    ├─> Selects Language (EN/FR)
    │
    ├─> Clicks "Load Data"
    │   └─> WHODataProcessor fetches:
    │       ├─> Alcohol consumption (2000-2022)
    │       └─> Alcohol disorders (by gender)
    │
    ├─> Explores 6 Tabs:
    │   ├─> 📊 Overview: Key metrics + regional chart
    │   ├─> 🍷 Consumption: Top 10 + World map + Europe trends
    │   ├─> 🏥 Disorders: Gender comparison by region
    │   ├─> 🔗 Correlations: Scatter plot + R² analysis
    │   ├─> 🌍 Regional: Regional averages table + chart
    │   └─> 📄 Export: Generate HTML report button
    │
    └─> Generates Report (optional)
        └─> HTMLReportGenerator creates bilingual HTML
            └─> Downloads complete report
```

## File Structure

```
who_alcohol_streamlit/
│
├── streamlit_app.py          # Main Streamlit UI (6 tabs)
├── requirements.txt          # Minimal dependencies
├── README.md                 # Documentation
├── verify_setup.py           # Setup checker
│
├── config/
│   ├── __init__.py
│   ├── settings.py          # API endpoints, constants
│   └── translations.py      # EN/FR translations dict
│
└── core/
    ├── __init__.py
    ├── data_processor.py    # WHO API data fetching
    └── report_generator.py  # HTML export with translations
```

## Key Components

### streamlit_app.py
- **Session State**: Manages data persistence
- **Language Switcher**: Sidebar selector (EN/FR)
- **Data Loading**: On-demand via button
- **6 Tabs**: Overview, Consumption, Disorders, Correlations, Regional, Export
- **Download**: Exports HTML report

### data_processor.py
- `fetch_all_data()`: Fetches consumption + disorders
- `get_top_consumers()`: Top N countries
- `get_regional_averages()`: Regional stats
- `get_europe_trend_data()`: Time series for EU
- `merge_consumption_disorder_data()`: For correlations

### report_generator.py
- `generate_report()`: Creates HTML with all charts
- Bilingual template support
- Plotly CDN integration
- Clean, printable format

### translations.py
- Complete EN/FR dictionaries
- All UI text translated
- Chart titles translated
- Export labels translated

## Removed from Original

❌ Dash framework
❌ Matplotlib/Seaborn
❌ Command-line interface
❌ Suicide data analysis
❌ Former drinkers data
❌ Clustering analysis
❌ Multiple execution modes
❌ Auto-generation on startup

## What's New

✅ Streamlit-native
✅ Complete bilingual support
✅ User-triggered workflows
✅ Session state management
✅ Clean, minimal codebase
✅ On-demand report generation
