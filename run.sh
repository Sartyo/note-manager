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
if [ ! -f ".env" ]; then
  echo "🔧 Creating default .env file..."
  cat <<EOF > .env
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:4200
EOF
fi

# Apply migrations
python manage.py migrate

# Collect static files (if needed)
# python manage.py collectstatic --noinput

# (Optional) Create superuser or load fixtures
# echo "Creating superuser..."
# python manage.py createsuperuser --noinput --username admin --email admin@example.com

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