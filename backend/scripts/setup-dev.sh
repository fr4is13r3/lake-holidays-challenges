#!/bin/bash
# Lake Holidays Challenge Backend - Development Setup Script

set -e  # Exit on any error

echo "🚀 Setting up Lake Holidays Challenge Backend Development Environment"

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then 
    echo "✅ Python $PYTHON_VERSION detected"
else
    echo "❌ Python $PYTHON_VERSION is too old. Please install Python 3.11 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🐳 Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed. Installing dependencies without Docker support."
    echo "   To use Docker features, please install Docker Desktop."
else
    echo "✅ Docker detected"
    
    # Check if docker-compose is available
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose detected"
    elif docker compose version &> /dev/null; then
        echo "✅ Docker Compose (v2) detected"
    else
        echo "⚠️  Docker Compose not found. Some features may not work."
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual configuration values"
fi

# Check if we can start services with Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 Starting database and Redis services..."
    docker-compose up -d postgres redis
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Run database migrations
    echo "🗄️  Running database migrations..."
    alembic upgrade head
    
    echo "✅ Backend setup complete!"
    echo ""
    echo "🎉 Your Lake Holidays Challenge backend is ready!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your configuration"
    echo "2. Start the development server: uvicorn app.main:app --reload"
    echo "3. Visit http://localhost:8000/docs for API documentation"
    echo ""
    echo "Useful commands:"
    echo "- Start all services: docker-compose up -d"
    echo "- View logs: docker-compose logs -f api"
    echo "- Stop services: docker-compose down"
    echo "- Run tests: pytest"
else
    echo "✅ Backend dependencies installed!"
    echo ""
    echo "⚠️  Docker not available. You'll need to:"
    echo "1. Install and configure PostgreSQL manually"
    echo "2. Install and configure Redis manually"
    echo "3. Update DATABASE_URL and REDIS_URL in .env"
    echo "4. Run: alembic upgrade head"
    echo "5. Start server: uvicorn app.main:app --reload"
fi
