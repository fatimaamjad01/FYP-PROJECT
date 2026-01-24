#!/bin/bash

# Script to deploy Prisma schema to Supabase

echo "🚀 Deploying Prisma schema to Supabase..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your DATABASE_URL"
    echo "See .env.example or SUPABASE_SETUP.md for more info"
    exit 1
fi

# Check if DATABASE_URL is set
if ! grep -q "DATABASE_URL" .env; then
    echo "❌ Error: DATABASE_URL not found in .env file!"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install --system -r requirements.txt

echo "🔧 Generating Prisma Client..."
npx prisma generate

echo "📤 Pushing schema to Supabase database..."
npx prisma db push --force-reset

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Schema successfully deployed to Supabase!"
    echo ""
    echo "Next steps:"
    echo "1. Run: uvicorn main:app --reload"
    echo "2. Visit: http://localhost:8000/docs"
else
    echo ""
    echo "❌ Failed to deploy schema. Please check your DATABASE_URL and try again."
fi
