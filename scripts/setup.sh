#!/bin/bash

# AITutor Setup Script
echo "🚀 Setting up AITutor..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Setup backend
echo "📦 Setting up backend..."
cd src/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../..

# Setup frontend
echo "📦 Setting up frontend..."
cd src/frontend
npm install
cd ../..

# Create environment files
echo "🔧 Creating environment files..."
cp src/backend/.env.example src/backend/.env
cp src/frontend/.env.example src/frontend/.env.local

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Add your OpenRouter API key to src/backend/.env"
echo "2. Run: cd src/backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"
echo "3. Run: cd src/frontend && npm run dev"
echo "4. Open http://localhost:3000"
