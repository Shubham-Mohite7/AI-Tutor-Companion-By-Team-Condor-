#!/bin/bash

# AITutor Start Script
echo "🚀 Starting AITutor..."

# Start backend
echo "🔧 Starting backend..."
cd src/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ../..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend..."
cd src/frontend
npm run dev &
FRONTEND_PID=$!
cd ../..

echo "✅ AITutor is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for Ctrl+C
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
