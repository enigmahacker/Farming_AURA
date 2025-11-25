#!/bin/bash
# Quick start script for Farming_AURA backend

set -e

echo "======================================"
echo "Farming_AURA Backend Quick Start"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
echo "🔗 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r backend/requirements.txt
pip install -q pytest pytest-asyncio

# Run tests
echo ""
echo "🧪 Running tests..."
cd backend
python -m pytest tests/test_api.py -v --tb=short
cd ..

# Start server
echo ""
echo "======================================"
echo "✅ All tests passed!"
echo "======================================"
echo ""
echo "🚀 Starting backend server..."
echo ""
echo "📍 API: http://localhost:8000"
echo "📍 Docs: http://localhost:8000/docs"
echo "📍 ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop."
echo ""

cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
