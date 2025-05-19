#!/bin/bash

set -e  # Exit on error

# === Backend Setup ===
echo "📦 Setting up Django backend..."

cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
  echo "📁 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment variables or config files
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "🔐 Generating SECRET_KEY and creating .env..."
    SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    echo "SECRET_KEY=${SECRET_KEY}" > "$ENV_FILE"
else
    echo "📄 .env file already exists."
fi

# Export environment variables
export $(grep -v '^#' .env | xargs)

# Apply migrations
python manage.py migrate

# Creating user for testing the app if it doesn't exists
echo "👤 Creating test user..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='test').exists():
    User.objects.create_user(username='test', password='test')
    print("✅ User 'test' created.")
else:
    print("ℹ️ User 'test' already exists.")
EOF

# Run backend server in background
echo "🚀 Starting Django server..."
python manage.py runserver &
BACKEND_PID=$!

cd ..

# === Frontend Setup ===
echo "🧰 Setting up Angular frontend..."

cd frontend

# Install Node dependencies
npm install

# Run Angular dev server in background
echo "🚀 Starting Angular dev server..."
npx ng serve &
FRONTEND_PID=$!

cd ..

# === Finalization ===
echo "✅ All services started."
echo "📡 Django:    http://127.0.0.1:8000"
echo "🌐 Angular:   http://localhost:4200"

# Wait for background processes (optional)
wait $BACKEND_PID $FRONTEND_PID