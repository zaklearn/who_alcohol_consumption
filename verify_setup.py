#!/usr/bin/env python3
"""
Quick verification script for WHO Streamlit Dashboard
"""

import sys
import subprocess

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import streamlit
        import pandas
        import plotly
        import requests
        import scipy
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_structure():
    """Check project structure"""
    print("🔍 Checking project structure...")
    
    import os
    required = [
        'streamlit_app.py',
        'config/settings.py',
        'config/translations.py',
        'core/data_processor.py',
        'core/report_generator.py'
    ]
    
    missing = [f for f in required if not os.path.exists(f)]
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    
    print("✅ Project structure OK")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("WHO Alcohol Analysis - Streamlit Dashboard")
    print("=" * 60)
    
    if check_dependencies() and check_structure():
        print("\n✅ Setup complete!")
        print("\n🚀 To start the dashboard, run:")
        print("   streamlit run streamlit_app.py")
        print("\n🌐 Dashboard will open at: http://localhost:8501")
        print("🇬🇧 🇫🇷  Language selector available in sidebar")
    else:
        print("\n❌ Setup incomplete. Fix errors above.")
        sys.exit(1)
