#!/bin/bash

# Script to run FastAPI application

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run ./deploy-to-supabase.sh first to set up the environment"
    exit 1
fi

# Activate virtual environment and run uvicorn
echo "🚀 Starting FastAPI server..."
source .venv/bin/activate
uvicorn main:app --reload
