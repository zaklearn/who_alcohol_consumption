#!/bin/bash
# Quick launch script for WHO Streamlit Dashboard

echo "🍷 WHO Alcohol Analysis - Streamlit Dashboard"
echo "=============================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if dependencies are installed
python3 verify_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Launching Streamlit dashboard..."
    echo ""
    streamlit run streamlit_app.py
else
    echo ""
    echo "❌ Setup verification failed."
    echo "Fix the issues above, then run: ./launch.sh"
fi
