#!/bin/bash
# BASIN::NEXUS - Quick Start Script

cd /Users/leonbasin/.gemini/antigravity/scratch/basin-signal-engine
source venv/bin/activate
echo "🚀 Starting BASIN::NEXUS..."
echo "📍 Open: http://localhost:8501"
streamlit run app.py --server.port 8501
