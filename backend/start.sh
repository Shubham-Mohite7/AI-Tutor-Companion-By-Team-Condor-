#!/bin/bash

# Set environment variables
export OPENROUTER_API_KEY=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

# Start the backend server
echo "Starting AITutor Backend with API key..."
python -m uvicorn app.main:app --reload --port 8000
