#!/bin/bash

# Self Assessment Portal Setup Script

set -e

echo "🚀 Self Assessment Portal Setup"
echo "================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python3 is installed
if ! command_exists python3; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if Docker is installed for Docker setup
if command_exists docker && command_exists docker-compose; then
    DOCKER_AVAILABLE=true
    echo "✅ Docker and Docker Compose are available"
else
    DOCKER_AVAILABLE=false
    echo "⚠️  Docker not available - local setup only"
fi

echo ""
echo "Choose setup method:"
echo "1) Local development (with virtual environment)"
echo "2) Docker development (recommended)"
echo "3) Production Docker setup"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🔧 Setting up local development environment..."
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "newenv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv newenv
        fi
        
        # Activate virtual environment and install dependencies
        echo "Activating virtual environment and installing dependencies..."
        source newenv/bin/activate
        pip install -r requirements.txt
        
        # Create .env file if it doesn't exist
        if [ ! -f ".env" ]; then
            echo "Creating .env file from template..."
            cp .env.example .env
            echo "⚠️  Please edit .env file with your settings"
        fi
        
        echo "✅ Local setup complete!"
        echo "To run the application:"
        echo "  source newenv/bin/activate"
        echo "  python3 main.py"
        ;;
        
    2)
        if [ "$DOCKER_AVAILABLE" = false ]; then
            echo "❌ Docker is not available. Please install Docker and Docker Compose first."
            exit 1
        fi
        
        echo "🐳 Setting up Docker development environment..."
        
        # Build and start services
        docker-compose build
        docker-compose up -d
        
        echo "✅ Docker development setup complete!"
        echo "🌐 Application available at: http://localhost:5002"
        echo "📊 MongoDB Admin available at: http://localhost:8081"
        echo ""
        echo "To stop services: docker-compose down"
        echo "To view logs: docker-compose logs -f"
        ;;
        
    3)
        if [ "$DOCKER_AVAILABLE" = false ]; then
            echo "❌ Docker is not available. Please install Docker and Docker Compose first."
            exit 1
        fi
        
        echo "🚀 Setting up production Docker environment..."
        
        # Build and start production services
        docker-compose -f docker-compose.prod.yml build
        docker-compose -f docker-compose.prod.yml up -d
        
        echo "✅ Production Docker setup complete!"
        echo "🌐 Application available at: http://localhost:5000"
        echo ""
        echo "To stop services: docker-compose -f docker-compose.prod.yml down"
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "📚 Default login credentials:"
echo "   Admin: admin/admin"
echo "   Student: student/student"
echo ""
echo "🎉 Setup completed successfully!"